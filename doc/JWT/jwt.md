# JWT

## JWT

### 组成

三部分组成，分别是：

1. header：主要声明了JWT的签名算法；
   * typ: 令牌的类型，即JWT
   * alg: 散列算法
   * jti: 代表了正在使用JWT的编号，这个编号在对应服务端应当唯一，也可以放在payload中

2. payload：主要承载了各种声明并传递明文数据
   * Registered Claims
   
     由使用JWT的那些标准化组织根据需要定义，建议但不强制使用，应当参考文档IANA JSON Web Token Registry
     * iss 【issuer】  签发人
     * sub 【subject】  主题，该JWT所面向的用户，用于处理特定应用，非常用字段
     * aud 【audience】  接受者
     * exp 【expiration】  无效/过期时间，该jwt销毁的时间；unix时间戳
     * nbf  【not before】  生效时间，该jwt的使用时间不能早于该时间；unix时间戳 
     * iat  【issued at】  该jwt的发布时间；unix 时间戳
     * jti  【JWT ID】  该jwt的唯一ID编号
   
   * Public Claims 
   
     可以添加任何的信息，一般添加用户的相关信息或其他业务需要的必要信息.但不建议添加敏感信息，因为该部分在客户端可解密.
     
   * Private Claims
   
     是提供者和消费者所共同定义的声明，一般不建议存放敏感信息，因为base64是对称解密的，意味着该部分信息可以归类为明文信息。

3. signature：拥有该部分的JWT被称为JWS，也就是签了名的JWS；没有该部分的JWT被称为nonsecure JWT 也就是不安全的JWT，此时header中声明的签名算法为none。

### 应用

* 认证 Authentication；
* 授权 Authorization // 注意这两个单词的区别；
* 联合识别；
* 客户端会话（无状态的会话）；
* 客户端机密。


## JWS
JWS就是JWT Signature，其结构就是在之前nonsecure JWT的基础上，根据头部声明签名算法，并在最后添加上签名。

* header

  描述关于该JWT的最基本的信息，例如其类型以及签名所用的算法等。 JSON内容要经Base64 编码生成字符串成为Header。

* PayLoad

  由JWT的标准所定义的，如iss、sub、aud、exp、lat

* signature

  这个部分header与payload通过header中声明的加密方式，使用密钥secret进行加密，生成签名。

JWS的主要目的是保证了数据在传输过程中不被篡改，验证数据的完整性。但由于仅采用Base64对消息内容编码，因此无法防止数据泄露。所以不适合用于传输敏感数据。

我们把JWT的密钥或者密钥对secret，统一称为JSON Web Key，也就是JWK。

签名算法有三种：
* 对称加密HMAC(哈希消息验证码)：HS256/HS384/HS512
* 非对称加密RSASSA(RSA签名算法):（RS256/RS384/RS512）
* ECDSA(椭圆曲线数据签名算法):（ES256/ES384/ES512）

### 多重验证与JWS序列化

当需要多重签名或者JOSE表头的对象与JWS混合的时候，往往需要用到JWS的序列化

## JWE

JWS是去验证数据的，而JWE（JSON Web Encryption）是保护数据不被第三方的人看到的。通过JWE，JWT变得更加安全。

JWS中，私钥持有者加密令牌，公钥持有者验证令牌。而JWE中，私钥一方应该是唯一可以解密令牌的一方。

在JWE中，公钥持有可以将新的数据放入JWT中，但是JWS中，公钥持有者只能验证数据，不能引入新的数据。因此，对于公钥/私钥的方案而言，JWS和JWE是互补的。

JWE一共有五个部分，分别是：
* The protected header，类似于JWS的头部；
* The encrypted key，用于加密密文和其他加密数据的对称密钥；
* The initialization vector，初始IV值，有些加密方式需要额外的或者随机的数据；
* The encrypted data (cipher text)，密文数据；
* The authentication tag，由算法产生的附加数据，来防止密文被篡改。

### JWE 密钥加密算法

一般来说，JWE需要对密钥进行加密，这就意味着同一个JWT中至少有两种加密算法在起作用。但是并非将密钥拿来就能用，我们需要对密钥进行加密后，利用JWK密钥管理模式来导出这些密钥。JWK的管理模式有以下五种，分别是：
* Key Encryption
* Key Wrapping
* Direct Key Agreement
* Key Agreement with Key Wrapping
* Direct Encryption

### JWE Header

就好像是JWS的头部一样。JWE的头部也有着自己规定的额外声明字段，如下所示：

* type：一般是 jwt
* alg：算法名称，和JWS相同，该算法用于加密稍后用于加密内容的实际密钥
* enc：算法名称，用上一步生成的密钥加密内容的算法。
* zip：加密前压缩数据的算法。该参数可选，如果不存在则不执行压缩，通常的值为 DEF，也就是deflate算法
* jku/jkw/kid/x5u/x5c/x5t/x5t#S256/typ/cty/crit：和JWS额额外声明一样。

### JWE 的加密过程
步骤2和步骤3，更具不同的密钥管理模式，应该有不同的处理方式。在此只罗列一些通常情况。

之前谈及，JWE一共有五个部分。现在来详细说一下加密的过程：

* 根据头部alg的声明，生成一定大小的随机数；
* 根据密钥管理模式确定加密密钥；
* 根据密钥管理模式确定JWE加密密钥，得到CEK；
* 计算初始IV，如果不需要，跳过此步骤；
* 如果ZIP头申明了，则压缩明文；
* 使用CEK，IV和附加认证数据，通过enc头声明的算法来加密内容，结果为加密数据和认证标记；
* 压缩内容，返回token。

JWE的计算过程相对繁琐，不够轻量级，因此适合与数据传输而非token认证，但该协议也足够安全可靠，用简短字符串描述了传输内容，兼顾数据的安全性与完整性。

### 多重验证与JWE序列化

* protected：之前的头部声明，利用b64uri加密；
* unprotected：一般放JWS的额外声明，这段内容不会被b64加密；
* iv：64加密后的iv参数；
* add：额外认证数据；
* ciphertext：b64加密后的加密数据；
* recipients：b64加密后的认证标志-加密链，这是一个数组，每个数组中包含了两个信息；
* header：主要是声明当前密钥的算法；
* encrypted_key：JWE加密密钥。
