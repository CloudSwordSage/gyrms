import JSEncrypt from 'jsencrypt'

export function encrypt(data: string, publicKey: string | null): string {
  if (!publicKey) {
    throw new Error('Public key is required for encryption')
  }
  if (data.length > 117) { // RSA加密最大长度限制
    throw new Error('密码过长，请限制在117个字符以内')
  }

  const encryptor = new JSEncrypt()
  encryptor.setPublicKey(publicKey)
  const encrypted = encryptor.encrypt(data)
  if (!encrypted) {
    throw new Error('加密失败，请检查公钥格式')
  }
  return encrypted
}
