// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.1 <0.9.0;

contract Test {
    uint public value;

    // 修改为支持接收 ETH 的构造函数
    constructor() payable {}

    function receiveETH() public payable {
        value = msg.value; // 保存接收的 ETH 数量
    }
}
