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
  default     = "ghcr.io/alain-david-001/fruitapi:0.4.0"
}

variable "allowed_cidr" {
  description = "CIDR block allowed to access FruitAPI on port 8000. Use your public IP with /32."
  type        = string
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
