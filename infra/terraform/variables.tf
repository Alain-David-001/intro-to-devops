variable "aws_region" {
  description = "AWS region for FruitAPI infrastructure."
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Name prefix for AWS resources."
  type        = string
  default     = "fruitapi"
}

variable "container_image" {
  description = "FruitAPI container image to run on ECS."
  type        = string
  default     = "ghcr.io/alain-david-001/fruitapi:0.5.0"
}

variable "allowed_cidr" {
  description = "CIDR block allowed to access the FruitAPI load balancer on port 80. Use your public IP with /32."
  type        = string
}

variable "app_replicas" {
  description = "Number of FruitAPI ECS tasks to run."
  type        = number
  default     = 2
}

variable "db_name" {
  description = "MySQL database name."
  type        = string
  default     = "fruitapi"
}

variable "db_username" {
  description = "MySQL application username."
  type        = string
  default     = "fruitapi"
}
