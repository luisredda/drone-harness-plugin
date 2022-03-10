if [ -z $1 ] ; then
   echo Informe a versão!
   python setup.py --version
   exit
fi
vrs=$1
echo VERSAO $vrs
docker build . -t drone-harness-plugin-trigger:$vrs 
docker tag drone-harness-plugin-trigger:$vrs 433522406042.dkr.ecr.us-east-1.amazonaws.com/drone-harness-plugin-trigger:latest
docker tag drone-harness-plugin-trigger:$vrs 433522406042.dkr.ecr.us-east-1.amazonaws.com/drone-harness-plugin-trigger:$vrs
# docker push 433522406042.dkr.ecr.us-east-1.amazonaws.com/drone-harness-plugin-trigger:$vrs
# docker push 433522406042.dkr.ecr.us-east-1.amazonaws.com/drone-harness-plugin-trigger:latest
docker save -o /tmp/drone-harness-plugin-trigger-$vrs.tar drone-harness-plugin-trigger:$vrs
scp -i ~/chaves/original-bastion.pem /tmp/drone-harness-plugin-trigger-$vrs.tar ec2-user@10.220.100.23:/tmp
echo LOAD
ssh -i ~/chaves/original-bastion.pem ec2-user@10.220.100.23 bash -c "/home/ec2-user/login.sh"
ssh -i ~/chaves/original-bastion.pem ec2-user@10.220.100.23 docker load -i /tmp/drone-harness-plugin-trigger-$vrs.tar
echo TAG 1
ssh -i ~/chaves/original-bastion.pem ec2-user@10.220.100.23 docker tag   drone-harness-plugin-trigger:$vrs 587897644671.dkr.ecr.sa-east-1.amazonaws.com/drone-harness-plugin-trigger:latest
echo TAG 2
ssh -i ~/chaves/original-bastion.pem ec2-user@10.220.100.23 docker tag   drone-harness-plugin-trigger:$vrs 587897644671.dkr.ecr.sa-east-1.amazonaws.com/drone-harness-plugin-trigger:$vrs
echo push 1
ssh -i ~/chaves/original-bastion.pem ec2-user@10.220.100.23 docker push   587897644671.dkr.ecr.sa-east-1.amazonaws.com/drone-harness-plugin-trigger:latest
echo push 2
ssh -i ~/chaves/original-bastion.pem ec2-user@10.220.100.23 docker push   587897644671.dkr.ecr.sa-east-1.amazonaws.com/drone-harness-plugin-trigger:$vrs

