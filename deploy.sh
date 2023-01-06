fission spec init
fission env create --spec --name onb-us-pep-env --image nexus.sigame.com.br/fission-onboarding-us-politically-exposed:0.1.0 --poolsize 0 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-us-pep-fn --env onb-us-pep-env --code fission.py --targetcpu 80 --executortype newdeploy --maxscale 3 --requestsperpod 10000 --spec
fission route create --spec --name onb-us-pep-rt --method PUT --url /onboarding/politically_exposed_us --function onb-us-pep-fn