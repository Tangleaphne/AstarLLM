**THIS CHECKLIST IS NOT COMPLETE**. Use `--show-ignored-findings` to show all the results.
Summary
 - [weak-prng](#weak-prng) (1 results) (High)
 - [incorrect-equality](#incorrect-equality) (2 results) (Medium)
 - [reentrancy-no-eth](#reentrancy-no-eth) (3 results) (Medium)
 - [missing-zero-check](#missing-zero-check) (5 results) (Low)
 - [reentrancy-benign](#reentrancy-benign) (3 results) (Low)
 - [reentrancy-events](#reentrancy-events) (3 results) (Low)
 - [timestamp](#timestamp) (7 results) (Low)
 - [assembly](#assembly) (2 results) (Informational)
 - [solc-version](#solc-version) (2 results) (Informational)
 - [low-level-calls](#low-level-calls) (1 results) (Informational)
 - [naming-convention](#naming-convention) (10 results) (Informational)
 - [too-many-digits](#too-many-digits) (1 results) (Informational)
## weak-prng
Impact: High
Confidence: Medium
 - [ ] ID-0
[UniswapV2Pair._update(uint256,uint256,uint112,uint112)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L527-L553) uses a weak PRNG: "[blockTimestamp = uint32(block.timestamp % 2 ** 32)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L531)" 

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L527-L553


## incorrect-equality
Impact: Medium
Confidence: High
 - [ ] ID-1
[UniswapV2Pair._safeTransfer(address,address,uint256)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L469-L475) uses a dangerous strict equality:
	- [require(bool,string)(success && (data.length == 0 || abi.decode(data,(bool))),UniswapV2: TRANSFER_FAILED)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L473)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L469-L475


 - [ ] ID-2
[UniswapV2Pair.mint(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L601-L643) uses a dangerous strict equality:
	- [_totalSupply == 0](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L619)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L601-L643


## reentrancy-no-eth
Impact: Medium
Confidence: Medium
 - [ ] ID-3
Reentrancy in [UniswapV2Pair.swap(uint256,uint256,address,bytes)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L699-L755):
	External calls:
	- [_safeTransfer(_token0,to,amount0Out)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L721)
		- [(success,data) = token.call(abi.encodeWithSelector(SELECTOR,to,value))](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L471)
	- [_safeTransfer(_token1,to,amount1Out)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L723)
		- [(success,data) = token.call(abi.encodeWithSelector(SELECTOR,to,value))](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L471)
	- [IUniswapV2Callee(to).uniswapV2Call(msg.sender,amount0Out,amount1Out,data)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L725)
	State variables written after the call(s):
	- [_update(balance0,balance1,_reserve0,_reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L751)
		- [blockTimestampLast = blockTimestamp](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L549)
	[UniswapV2Pair.blockTimestampLast](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L429) can be used in cross function reentrancies:
	- [UniswapV2Pair._update(uint256,uint256,uint112,uint112)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L527-L553)
	- [UniswapV2Pair.getReserves()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L457-L465)
	- [_update(balance0,balance1,_reserve0,_reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L751)
		- [reserve0 = uint112(balance0)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L545)
	[UniswapV2Pair.reserve0](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L425) can be used in cross function reentrancies:
	- [UniswapV2Pair._update(uint256,uint256,uint112,uint112)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L527-L553)
	- [UniswapV2Pair.burn(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L649-L693)
	- [UniswapV2Pair.getReserves()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L457-L465)
	- [UniswapV2Pair.mint(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L601-L643)
	- [UniswapV2Pair.skim(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L761-L771)
	- [UniswapV2Pair.sync()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L777-L781)
	- [_update(balance0,balance1,_reserve0,_reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L751)
		- [reserve1 = uint112(balance1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L547)
	[UniswapV2Pair.reserve1](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L427) can be used in cross function reentrancies:
	- [UniswapV2Pair._update(uint256,uint256,uint112,uint112)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L527-L553)
	- [UniswapV2Pair.burn(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L649-L693)
	- [UniswapV2Pair.getReserves()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L457-L465)
	- [UniswapV2Pair.mint(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L601-L643)
	- [UniswapV2Pair.skim(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L761-L771)
	- [UniswapV2Pair.sync()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L777-L781)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L699-L755


 - [ ] ID-4
Reentrancy in [UniswapV2Factory.createPair(address,address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L821-L851):
	External calls:
	- [IUniswapV2Pair(pair).initialize(token0,token1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L841)
	State variables written after the call(s):
	- [getPair[token0][token1] = pair](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L843)
	[UniswapV2Factory.getPair](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L795) can be used in cross function reentrancies:
	- [UniswapV2Factory.createPair(address,address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L821-L851)
	- [UniswapV2Factory.getPair](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L795)
	- [getPair[token1][token0] = pair](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L845)
	[UniswapV2Factory.getPair](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L795) can be used in cross function reentrancies:
	- [UniswapV2Factory.createPair(address,address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L821-L851)
	- [UniswapV2Factory.getPair](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L795)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L821-L851


 - [ ] ID-5
Reentrancy in [UniswapV2Pair.burn(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L649-L693):
	External calls:
	- [_safeTransfer(_token0,to,amount0)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L677)
		- [(success,data) = token.call(abi.encodeWithSelector(SELECTOR,to,value))](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L471)
	- [_safeTransfer(_token1,to,amount1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L679)
		- [(success,data) = token.call(abi.encodeWithSelector(SELECTOR,to,value))](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L471)
	State variables written after the call(s):
	- [_update(balance0,balance1,_reserve0,_reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L687)
		- [blockTimestampLast = blockTimestamp](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L549)
	[UniswapV2Pair.blockTimestampLast](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L429) can be used in cross function reentrancies:
	- [UniswapV2Pair._update(uint256,uint256,uint112,uint112)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L527-L553)
	- [UniswapV2Pair.getReserves()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L457-L465)
	- [kLast = uint256(reserve0).mul(reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L689)
	[UniswapV2Pair.kLast](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L437) can be used in cross function reentrancies:
	- [UniswapV2Pair._mintFee(uint112,uint112)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L559-L595)
	- [UniswapV2Pair.burn(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L649-L693)
	- [UniswapV2Pair.kLast](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L437)
	- [UniswapV2Pair.mint(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L601-L643)
	- [_update(balance0,balance1,_reserve0,_reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L687)
		- [reserve0 = uint112(balance0)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L545)
	[UniswapV2Pair.reserve0](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L425) can be used in cross function reentrancies:
	- [UniswapV2Pair._update(uint256,uint256,uint112,uint112)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L527-L553)
	- [UniswapV2Pair.burn(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L649-L693)
	- [UniswapV2Pair.getReserves()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L457-L465)
	- [UniswapV2Pair.mint(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L601-L643)
	- [UniswapV2Pair.skim(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L761-L771)
	- [UniswapV2Pair.sync()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L777-L781)
	- [_update(balance0,balance1,_reserve0,_reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L687)
		- [reserve1 = uint112(balance1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L547)
	[UniswapV2Pair.reserve1](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L427) can be used in cross function reentrancies:
	- [UniswapV2Pair._update(uint256,uint256,uint112,uint112)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L527-L553)
	- [UniswapV2Pair.burn(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L649-L693)
	- [UniswapV2Pair.getReserves()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L457-L465)
	- [UniswapV2Pair.mint(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L601-L643)
	- [UniswapV2Pair.skim(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L761-L771)
	- [UniswapV2Pair.sync()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L777-L781)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L649-L693


## missing-zero-check
Impact: Low
Confidence: Medium
 - [ ] ID-6
[UniswapV2Factory.setFeeTo(address)._feeTo](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L855) lacks a zero-check on :
		- [feeTo = _feeTo](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L859)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L855


 - [ ] ID-7
[UniswapV2Factory.constructor(address)._feeToSetter](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L805) lacks a zero-check on :
		- [feeToSetter = _feeToSetter](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L807)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L805


 - [ ] ID-8
[UniswapV2Factory.setFeeToSetter(address)._feeToSetter](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L865) lacks a zero-check on :
		- [feeToSetter = _feeToSetter](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L869)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L865


 - [ ] ID-9
[UniswapV2Pair.initialize(address,address)._token0](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L513) lacks a zero-check on :
		- [token0 = _token0](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L517)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L513


 - [ ] ID-10
[UniswapV2Pair.initialize(address,address)._token1](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L513) lacks a zero-check on :
		- [token1 = _token1](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L519)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L513


## reentrancy-benign
Impact: Low
Confidence: Medium
 - [ ] ID-11
Reentrancy in [UniswapV2Factory.createPair(address,address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L821-L851):
	External calls:
	- [IUniswapV2Pair(pair).initialize(token0,token1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L841)
	State variables written after the call(s):
	- [allPairs.push(pair)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L847)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L821-L851


 - [ ] ID-12
Reentrancy in [UniswapV2Pair.burn(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L649-L693):
	External calls:
	- [_safeTransfer(_token0,to,amount0)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L677)
		- [(success,data) = token.call(abi.encodeWithSelector(SELECTOR,to,value))](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L471)
	- [_safeTransfer(_token1,to,amount1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L679)
		- [(success,data) = token.call(abi.encodeWithSelector(SELECTOR,to,value))](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L471)
	State variables written after the call(s):
	- [_update(balance0,balance1,_reserve0,_reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L687)
		- [price0CumulativeLast += uint256(UQ112x112.encode(_reserve1).uqdiv(_reserve0)) * timeElapsed](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L539)
	- [_update(balance0,balance1,_reserve0,_reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L687)
		- [price1CumulativeLast += uint256(UQ112x112.encode(_reserve0).uqdiv(_reserve1)) * timeElapsed](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L541)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L649-L693


 - [ ] ID-13
Reentrancy in [UniswapV2Pair.swap(uint256,uint256,address,bytes)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L699-L755):
	External calls:
	- [_safeTransfer(_token0,to,amount0Out)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L721)
		- [(success,data) = token.call(abi.encodeWithSelector(SELECTOR,to,value))](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L471)
	- [_safeTransfer(_token1,to,amount1Out)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L723)
		- [(success,data) = token.call(abi.encodeWithSelector(SELECTOR,to,value))](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L471)
	- [IUniswapV2Callee(to).uniswapV2Call(msg.sender,amount0Out,amount1Out,data)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L725)
	State variables written after the call(s):
	- [_update(balance0,balance1,_reserve0,_reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L751)
		- [price0CumulativeLast += uint256(UQ112x112.encode(_reserve1).uqdiv(_reserve0)) * timeElapsed](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L539)
	- [_update(balance0,balance1,_reserve0,_reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L751)
		- [price1CumulativeLast += uint256(UQ112x112.encode(_reserve0).uqdiv(_reserve1)) * timeElapsed](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L541)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L699-L755


## reentrancy-events
Impact: Low
Confidence: Medium
 - [ ] ID-14
Reentrancy in [UniswapV2Factory.createPair(address,address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L821-L851):
	External calls:
	- [IUniswapV2Pair(pair).initialize(token0,token1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L841)
	Event emitted after the call(s):
	- [PairCreated(token0,token1,pair,allPairs.length)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L849)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L821-L851


 - [ ] ID-15
Reentrancy in [UniswapV2Pair.swap(uint256,uint256,address,bytes)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L699-L755):
	External calls:
	- [_safeTransfer(_token0,to,amount0Out)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L721)
		- [(success,data) = token.call(abi.encodeWithSelector(SELECTOR,to,value))](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L471)
	- [_safeTransfer(_token1,to,amount1Out)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L723)
		- [(success,data) = token.call(abi.encodeWithSelector(SELECTOR,to,value))](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L471)
	- [IUniswapV2Callee(to).uniswapV2Call(msg.sender,amount0Out,amount1Out,data)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L725)
	Event emitted after the call(s):
	- [Swap(msg.sender,amount0In,amount1In,amount0Out,amount1Out,to)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L753)
	- [Sync(reserve0,reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L551)
		- [_update(balance0,balance1,_reserve0,_reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L751)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L699-L755


 - [ ] ID-16
Reentrancy in [UniswapV2Pair.burn(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L649-L693):
	External calls:
	- [_safeTransfer(_token0,to,amount0)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L677)
		- [(success,data) = token.call(abi.encodeWithSelector(SELECTOR,to,value))](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L471)
	- [_safeTransfer(_token1,to,amount1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L679)
		- [(success,data) = token.call(abi.encodeWithSelector(SELECTOR,to,value))](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L471)
	Event emitted after the call(s):
	- [Burn(msg.sender,amount0,amount1,to)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L691)
	- [Sync(reserve0,reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L551)
		- [_update(balance0,balance1,_reserve0,_reserve1)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L687)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L649-L693


## timestamp
Impact: Low
Confidence: Medium
 - [ ] ID-17
[UniswapV2Pair.burn(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L649-L693) uses timestamp for comparisons
	Dangerous comparisons:
	- [require(bool,string)(amount0 > 0 && amount1 > 0,UniswapV2: INSUFFICIENT_LIQUIDITY_BURNED)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L673)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L649-L693


 - [ ] ID-18
[UniswapV2ERC20.permit(address,address,uint256,uint256,uint8,bytes32,bytes32)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L373-L397) uses timestamp for comparisons
	Dangerous comparisons:
	- [require(bool,string)(deadline >= block.timestamp,UniswapV2: EXPIRED)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L375)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L373-L397


 - [ ] ID-19
[UniswapV2Pair._safeTransfer(address,address,uint256)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L469-L475) uses timestamp for comparisons
	Dangerous comparisons:
	- [require(bool,string)(success && (data.length == 0 || abi.decode(data,(bool))),UniswapV2: TRANSFER_FAILED)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L473)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L469-L475


 - [ ] ID-20
[UniswapV2Pair._mintFee(uint112,uint112)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L559-L595) uses timestamp for comparisons
	Dangerous comparisons:
	- [rootK > rootKLast](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L575)
	- [liquidity > 0](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L583)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L559-L595


 - [ ] ID-21
[UniswapV2Pair._update(uint256,uint256,uint112,uint112)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L527-L553) uses timestamp for comparisons
	Dangerous comparisons:
	- [timeElapsed > 0 && _reserve0 != 0 && _reserve1 != 0](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L535)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L527-L553


 - [ ] ID-22
[UniswapV2Pair.mint(address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L601-L643) uses timestamp for comparisons
	Dangerous comparisons:
	- [_totalSupply == 0](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L619)
	- [require(bool,string)(liquidity > 0,UniswapV2: INSUFFICIENT_LIQUIDITY_MINTED)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L631)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L601-L643


 - [ ] ID-23
[UniswapV2Pair.swap(uint256,uint256,address,bytes)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L699-L755) uses timestamp for comparisons
	Dangerous comparisons:
	- [require(bool,string)(amount0Out < _reserve0 && amount1Out < _reserve1,UniswapV2: INSUFFICIENT_LIQUIDITY)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L705)
	- [require(bool,string)(amount0In > 0 || amount1In > 0,UniswapV2: INSUFFICIENT_INPUT_AMOUNT)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L737)
	- [require(bool,string)(balance0Adjusted.mul(balance1Adjusted) >= uint256(_reserve0).mul(_reserve1).mul(1000 ** 2),UniswapV2: K)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L745)
	- [balance0 > _reserve0 - amount0Out](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L733)
	- [balance1 > _reserve1 - amount1Out](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L735)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L699-L755


## assembly
Impact: Informational
Confidence: High
 - [ ] ID-24
[UniswapV2Factory.createPair(address,address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L821-L851) uses assembly
	- [INLINE ASM](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L835-L839)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L821-L851


 - [ ] ID-25
[UniswapV2ERC20.constructor()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L259-L287) uses assembly
	- [INLINE ASM](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L263-L267)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L259-L287


## solc-version
Impact: Informational
Confidence: High
 - [ ] ID-26
solc-0.5.16 is an outdated solc version. Use a more recent version (at least 0.8.0), if possible.

 - [ ] ID-27
Version constraint =0.5.16 contains known severe issues (https://solidity.readthedocs.io/en/latest/bugs.html)
	- AbiReencodingHeadOverflowWithStaticArrayCleanup
	- DirtyBytesArrayToStorage
	- NestedCalldataArrayAbiReencodingSizeValidation
	- ABIDecodeTwoDimensionalArrayMemory
	- KeccakCaching
	- EmptyByteArrayCopy
	- DynamicArrayCleanup
	- MissingEscapingInFormatting
	- ImplicitConstructorCallvalueCheck
	- TupleAssignmentMultiStackSlotComponents
	- MemoryArrayCreationOverflow
	- privateCanBeOverridden.
It is used by:
	- [=0.5.16](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L1)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L1


## low-level-calls
Impact: Informational
Confidence: High
 - [ ] ID-28
Low level call in [UniswapV2Pair._safeTransfer(address,address,uint256)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L469-L475):
	- [(success,data) = token.call(abi.encodeWithSelector(SELECTOR,to,value))](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L471)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L469-L475


## naming-convention
Impact: Informational
Confidence: High
 - [ ] ID-29
Function [IUniswapV2ERC20.DOMAIN_SEPARATOR()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L169) is not in mixedCase

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L169


 - [ ] ID-30
Function [IUniswapV2Pair.PERMIT_TYPEHASH()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L69) is not in mixedCase

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L69


 - [ ] ID-31
Function [IUniswapV2Pair.MINIMUM_LIQUIDITY()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L103) is not in mixedCase

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L103


 - [ ] ID-32
Parameter [UniswapV2Factory.setFeeToSetter(address)._feeToSetter](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L865) is not in mixedCase

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L865


 - [ ] ID-33
Function [IUniswapV2Pair.DOMAIN_SEPARATOR()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L67) is not in mixedCase

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L67


 - [ ] ID-34
Function [IUniswapV2ERC20.PERMIT_TYPEHASH()](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L171) is not in mixedCase

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L171


 - [ ] ID-35
Variable [UniswapV2ERC20.DOMAIN_SEPARATOR](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L243) is not in mixedCase

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L243


 - [ ] ID-36
Parameter [UniswapV2Pair.initialize(address,address)._token0](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L513) is not in mixedCase

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L513


 - [ ] ID-37
Parameter [UniswapV2Pair.initialize(address,address)._token1](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L513) is not in mixedCase

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L513


 - [ ] ID-38
Parameter [UniswapV2Factory.setFeeTo(address)._feeTo](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L855) is not in mixedCase

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L855


## too-many-digits
Impact: Informational
Confidence: Medium
 - [ ] ID-39
[UniswapV2Factory.createPair(address,address)](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L821-L851) uses literals with too many digits:
	- [bytecode = type(address)(UniswapV2Pair).creationCode](../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L831)

../../share/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f.sol#L821-L851


