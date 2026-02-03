resource "aws_ecr_repository" "spine" {
  name                 = "vte/spine"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "web" {
  name                 = "vte/web"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "ecr_spine_url" {
  value = aws_ecr_repository.spine.repository_url
}

output "ecr_web_url" {
  value = aws_ecr_repository.web.repository_url
}
