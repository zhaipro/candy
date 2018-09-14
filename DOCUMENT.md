## 以太坊

1. `以太坊（Ethereum）`是一个允许任何人在其上创建和使用分布式应用的开放的区块链平台。
1. `以太币（Ether）`是以太坊中通用的货币，它的主要用途是用来购买 `EVM` 中执行指令所消耗的汽油（Gas）。在交易行中以太币被缩写为`ETH`。

### 以太币的单位

![](http://latex.codecogs.com/gif.latex?1\\mathbf{Ether}=10^{18}\\mathbf{Wei})

![](http://latex.codecogs.com/gif.latex?1\\mathbf{GWei}=10^9\\mathbf{Wei})

不同的场景下习惯使用不同的单位，通常交易行都是以 Ether 为单位，计算 Gas 价格时一般使用 GWei，在以太坊代码开发中使用最基本的单位 Wei。

[以太币(Ether)的单位](https://zhuanlan.zhihu.com/p/28994731)


## 设定执行以太坊智能合约提供的费用

为执行一个合约，需要支付费用。

需要支付的费用 = 步数 * 费用/单步

你发出的命令需要包括两个与费用相关的值：

1. gasPrice：费用/单步（用以太币计算）
1. gas：能支付的上限

### web3.py
```
web3.Web3.toWei(number:int, unit:str) -> int
Docstring: Takes a number of a unit and converts it to wei.
```
```
web3.Web3.fromWei(number:int, unit:str) -> Union[int, decimal.Decimal]
Docstring: Takes a number of wei and converts it to any other ether unit.
```
