"""
KMS policy constants
"""

# Actions that can be used in a key policy, that do not expose secrets
IAM_SAFE_ACTIONS = [
    # Read actions
    "kms:Describe*",
    "kms:List*",
    "kms:Get*",

    # Safe operations
    "kms:EnableKey",
    "kms:EnableKeyRotation",
    "kms:UpdateKeyDescription",
    "kms:DisableKeyRotation",
    "kms:TagResource",
    "kms:UntagResource",
    "kms:CancelKeyDeletion",

    # Safe because they can be only used to create
    "kms:CreateAlias",
    "kms:CreateKey",
    "kms:ImportKeyMaterial",

    # Allow encrypting
    "kms:Encrypt",
    "kms:GenerateDataKey",
    "kms:GenerateDataKeyWithoutPlaintext",
    "kms:GenerateRandom",
    "kms:ReEncrypt*",

    # These can break an application, but cannot allow decryption
    "kms:UpdateAlias",
    "kms:DeleteAlias",
    "kms:DisableKey",
    "kms:ScheduleKeyDeletion",

    # These can break an application in an hard to recover way, but cannot allow decryption
    "kms:RevokeGrant",
    "kms:DeleteImportedKeyMaterial",

    # Not: CreateGrant, PutKeyPolicy, they can be used for escalation
    # Not: Decrypt, it can be used to read the secrets
]

# Actions that can be used in a key policy, that a decryptor may need
IAM_DECRYPT_ACTIONS = [
    # The decryptor should not be able to change the plaintext
    "kms:Decrypt",
    "kms:ReEncrypt*",
    "kms:DescribeKey",
]
