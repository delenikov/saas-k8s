Write-Host "========================================="
Write-Host " CLOUD COST LEFTOVER CHECK"
Write-Host "========================================="
Write-Host ""

# --------------------------------------------------
# AWS CHECKS
# --------------------------------------------------

Write-Host "========== AWS / EKS ==========" -ForegroundColor Cyan

try {

    Write-Host "`n[EKS Clusters]"
    aws eks list-clusters

    Write-Host "`n[Running EC2 Instances]"
    aws ec2 describe-instances `
        --filters Name=instance-state-name,Values=running `
        --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name]' `
        --output table

    Write-Host "`n[Load Balancers v2]"
    aws elbv2 describe-load-balancers `
        --query 'LoadBalancers[*].[LoadBalancerName,Type,State.Code]' `
        --output table

    Write-Host "`n[Classic Load Balancers]"
    aws elb describe-load-balancers `
        --query 'LoadBalancerDescriptions[*].[LoadBalancerName,DNSName]' `
        --output table

    Write-Host "`n[Elastic IPs]"
    aws ec2 describe-addresses `
        --query 'Addresses[*].[PublicIp,AllocationId,AssociationId]' `
        --output table

    Write-Host "`n[EBS Volumes]"
    aws ec2 describe-volumes `
        --query 'Volumes[*].[VolumeId,State,Size]' `
        --output table

    Write-Host "`n[EBS Snapshots]"
    aws ec2 describe-snapshots `
        --owner-ids self `
        --query 'Snapshots[*].[SnapshotId,VolumeSize,StartTime]' `
        --output table

    Write-Host "`n[NAT Gateways]"
    aws ec2 describe-nat-gateways `
        --query 'NatGateways[*].[NatGatewayId,State]' `
        --output table

    Write-Host "`n[VPCs]"
    aws ec2 describe-vpcs `
        --query 'Vpcs[*].[VpcId,CidrBlock]' `
        --output table

    Write-Host "`n[CloudWatch Log Groups]"
    aws logs describe-log-groups `
        --query 'logGroups[*].[logGroupName,storedBytes]' `
        --output table

}
catch {
    Write-Host "AWS CLI check failed." -ForegroundColor Red
}

# --------------------------------------------------
# AZURE CHECKS
# --------------------------------------------------

Write-Host ""
Write-Host "========== AZURE / AKS ==========" -ForegroundColor Cyan

try {

    Write-Host "`n[AKS Clusters]"
    az aks list -o table

    Write-Host "`n[Resource Groups]"
    az group list -o table

    Write-Host "`n[Virtual Machines]"
    az vm list -d -o table

    Write-Host "`n[VM Scale Sets]"
    az vmss list -o table

    Write-Host "`n[Load Balancers]"
    az network lb list -o table

    Write-Host "`n[Public IPs]"
    az network public-ip list `
        --query "[].{Name:name,IP:ipAddress,Attached:ipConfiguration!=null}" `
        -o table

    Write-Host "`n[Managed Disks]"
    az disk list -o table 
    az resource list --resource-type "Microsoft.Compute/disks" -o table

    Write-Host "`n[Snapshots]"
    az snapshot list -o table

    Write-Host "`n[NAT Gateways]"
    az network nat gateway list -o table

    Write-Host "`n[Log Analytics Workspaces]"
    az monitor log-analytics workspace list -o table

    Write-Host "`n[ALL Azure Resources]"
    az resource list -o table

}
catch {
    Write-Host "Azure CLI check failed." -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================="
Write-Host " CHECK COMPLETE"
Write-Host "========================================="