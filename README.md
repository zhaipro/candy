

## 依赖

1. Python: 3.6
1. 及其他

## Docker

我使用了阿里云提供的 [容器镜像服务](https://www.aliyun.com/product/containerservice) 来构建 Docker 镜像，并公开了下载权限，下载地址是：

1. 公网地址：`registry.cn-beijing.aliyuncs.com/dayifu/candy`
1. 经典内网：`registry-internal.cn-beijing.aliyuncs.com/dayifu/candy`

如果在自行构建竟像时，觉得等待的时间太长，可回到 [release-v0.1](https://github.com/zhaipro/candy/tree/release-v0.1)，看一下原来的 [Dockerfile](https://github.com/zhaipro/candy/blob/release-v0.1/Dockerfile)。因为现在使用阿里云提供的构建方式，所以已不在需要原来多余的优化方式了。


[文档](./DOCUMENT.md)
