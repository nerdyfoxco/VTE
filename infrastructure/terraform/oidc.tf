# 1. Create OIDC Provider for GitHub
resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"] # GitHub's Thumbprint
}

# 2. Create IAM Role for Actions
resource "aws_iam_role" "github_actions" {
  name = "vte-github-actions-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRoleWithWebIdentity"
        Effect = "Allow"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        }
        Condition = {
          StringLike = {
            "token.actions.githubusercontent.com:sub" : "repo:nerdyfoxco/VTE:*"
          }
        }
      }
    ]
  })
}

# 3. Policy: Allow Pushing to ECR
resource "aws_iam_policy" "ecr_push" {
  name        = "vte-ecr-push-policy"
  description = "Allow GitHub Actions to push to ECR"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:GetRepositoryPolicy",
          "ecr:DescribeRepositories",
          "ecr:ListImages",
          "ecr:DescribeImages",
          "ecr:BatchGetImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload",
          "ecr:PutImage"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_ecr" {
  role       = aws_iam_role.github_actions.name
  policy_arn = aws_iam_policy.ecr_push.arn
}

output "github_actions_role_arn" {
  value = aws_iam_role.github_actions.arn
}
