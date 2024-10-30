locals {
  resource_location = "West US 2"
}

variable "resource_prefix" {
  description = "Prefix for all resources"
  type        = string
}

variable "azure_subscription_id" {
  description = "Azure subscription id"
  type        = string
}


data "azurerm_subscription" "primary" {}
data "azurerm_client_config" "current" {}


resource "azurerm_resource_group" "content_safety" {
  name     = "${var.resource_prefix}_content_safety_rg"
  location = local.resource_location
}

resource "azurerm_cognitive_account" "content-safety" {
  name                = "${var.resource_prefix}_content_safety"
  location            = azurerm_resource_group.content_safety.location
  resource_group_name = azurerm_resource_group.content_safety.name
  kind                = "ContentSafety"
  sku_name            = "S0"
}
