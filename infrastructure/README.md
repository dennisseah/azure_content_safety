# Infrastructure

## Terraform
install terraform from [here](https://learn.hashicorp.com/tutorials/terraform/install-cli)

## Azure Login

```bash
az login
az account set --subscription <SUBSCRIPTION_ID>
az account show
```
make sure you have the correct subscription selected

## Terraform Init, validate and plan

Make a file called `terraform.tfvars`.
Add a variable `resource_prefix = <uniq-name>`, for example your handle like 'joesmith' or 'janedoe'

All the setup with `terraform` can then be handled with

```bash
terraform init
terraform validate
terraform plan -out plan.tfplan
terraform apply plan.tfplan
```

# Remove all resources

```bash
terraform destroy
```