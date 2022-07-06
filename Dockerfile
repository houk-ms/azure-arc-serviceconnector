FROM mcr.microsoft.com/azure-cli:2.36.0

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pytest pytest-xdist filelock junit_xml kubernetes==11.0.0 azure.identity msrestazure azure-mgmt-hybridkubernetes azure-mgmt-kubernetesconfiguration==2.0.0

RUN az extension add --name k8s-extension --yes --debug

RUN /usr/bin/curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl \
    && chmod +x ./kubectl  \
    &&  mv ./kubectl /usr/local/bin/kubectl

COPY ./ /conformancetests/
RUN ls -la /conformancetests/*

RUN ["chmod", "+x", "/conformancetests/arc_conformance.sh"]
ENTRYPOINT ["/conformancetests/arc_conformance.sh"]
