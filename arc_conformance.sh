#!/bin/bash
set -ex

results_dir="/tmp/sonobuoy/results"

# App Registration: ServiceLinkerArcExtensionConformanceTest
CLIENT_ID='8caf986f-fbc5-4205-9a83-9f6fe1075bb9'
TENANT_ID='72f988bf-86f1-41af-91ab-2d7cd011db47'
SUBSCRIPTION_ID='937bc588-a144-4083-8612-5f9ffbbddb14'
RESOURCE_GROUP='servicelinker-test-linux-group'
CLUSTER_NAME='test-scextension-cluster'


if [[ -z "${CLIENT_SECRET}" ]]; then
  echo "ERROR: parameter CLIENT_SECRET is required." > ${results_dir}/error
fi


# saveResults prepares the results for handoff to the Sonobuoy worker.
saveResults() {
    # handle result
    python /conformancetests/tests/result_handler.py

    cd ${results_dir}
    # Sonobuoy worker expects a tar file.
    tar czf results.tar.gz *
    # Signal to the worker that we are done and where to find the results.
    printf ${results_dir}/results.tar.gz > ${results_dir}/done
}

# Ensure that we tell the Sonobuoy worker we are done regardless of results.
trap saveResults EXIT

# create or update the extension
createOrUpdateExtension() {
    az k8s-extension create \
      --resource-group  ${RESOURCE_GROUP} \
      --cluster-name ${CLUSTER_NAME} \
      --cluster-type managedClusters \
      --name sc-extension \
      --extension-type microsoft.servicelinker.connection \
      --scope cluster \
      --release-namespace sc-system \
      --release-train prod \
      --config-protected ${configs} 2> ${results_dir}/error
}

# delete the extension
deleteExtension() {
    az k8s-extension delete \
      --resource-group  ${RESOURCE_GROUP} \
      --cluster-name ${CLUSTER_NAME} \
      --cluster-type managedClusters \
      --name sc-extension --yes 2> ${results_dir}/error
}


cd "/conformancetests"

az login --service-principal \
  -u ${CLIENT_ID} \
  -p ${CLIENT_SECRET} \
  --tenant ${TENANT_ID} 2> ${results_dir}/error

az account set \
  --subscription ${SUBSCRIPTION_ID} 2> ${results_dir}/error

# test create secret
configs=`python test_parameters/format_parameter.py test_parameters/test_create_secret.json`
createOrUpdateExtension
sleep 1m
python tests/check_resource_existance.py test_parameters/test_create_secret.json >${results_dir}/test_create_secret

# test update secret
configs=`python test_parameters/format_parameter.py test_parameters/test_update_secret.json`
createOrUpdateExtension
sleep 1m
python tests/check_resource_existance.py test_parameters/test_update_secret.json >${results_dir}/test_update_secret

# test delete secret
configs=`python test_parameters/format_parameter.py test_parameters/test_delete_secret.json`
deleteExtension
sleep 1m
python tests/check_resource_deletion.py test_parameters/test_delete_secret.json >${results_dir}/test_delete_secret

# test create csi
configs=`python test_parameters/format_parameter.py test_parameters/test_create_csi.json`
createOrUpdateExtension
sleep 1m
python tests/check_resource_existance.py test_parameters/test_create_csi.json >${results_dir}/test_create_csi

# test update csi
configs=`python test_parameters/format_parameter.py test_parameters/test_update_csi.json`
createOrUpdateExtension
sleep 1m
python tests/check_resource_existance.py test_parameters/test_update_csi.json >${results_dir}/test_update_csi

# test delete csi
configs=`python test_parameters/format_parameter.py test_parameters/test_delete_csi.json`
deleteExtension
sleep 1m
python tests/check_resource_deletion.py test_parameters/test_delete_csi.json >${results_dir}/test_delete_csi
