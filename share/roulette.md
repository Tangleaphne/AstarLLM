**THIS CHECKLIST IS NOT COMPLETE**. Use `--show-ignored-findings` to show all the results.
Summary
 - [controlled-array-length](#controlled-array-length) (1 results) (High)
 - [weak-prng](#weak-prng) (1 results) (High)
 - [uninitialized-storage](#uninitialized-storage) (1 results) (High)
 - [incorrect-equality](#incorrect-equality) (1 results) (Medium)
 - [timestamp](#timestamp) (2 results) (Low)
 - [deprecated-standards](#deprecated-standards) (2 results) (Informational)
 - [solc-version](#solc-version) (2 results) (Informational)
 - [reentrancy-unlimited-gas](#reentrancy-unlimited-gas) (1 results) (Informational)
 - [constable-states](#constable-states) (1 results) (Optimization)
## controlled-array-length
Impact: High
Confidence: Medium
 - [ ] ID-0
[CryptoRoulette](../../share/test.sol#L13-L61) contract sets array length with a user-controlled value:
	- [gamesPlayed.push(game)](../../share/test.sol#L42)

../../share/test.sol#L13-L61


## weak-prng
Impact: High
Confidence: Medium
 - [ ] ID-1
[CryptoRoulette.shuffle()](../../share/test.sol#L31-L34) uses a weak PRNG: "[secretNumber = uint8(sha3()(now,block.blockhash(block.number - 1))) % 20 + 1](../../share/test.sol#L33)" 

../../share/test.sol#L31-L34


## uninitialized-storage
Impact: High
Confidence: High
 - [ ] ID-2
[CryptoRoulette.play(uint256).game](../../share/test.sol#L39) is a storage variable never initialized

../../share/test.sol#L39


## incorrect-equality
Impact: Medium
Confidence: High
 - [ ] ID-3
[CryptoRoulette.play(uint256)](../../share/test.sol#L36-L51) uses a dangerous strict equality:
	- [number == secretNumber](../../share/test.sol#L44)

../../share/test.sol#L36-L51


## timestamp
Impact: Low
Confidence: Medium
 - [ ] ID-4
[CryptoRoulette.play(uint256)](../../share/test.sol#L36-L51) uses timestamp for comparisons
	Dangerous comparisons:
	- [number == secretNumber](../../share/test.sol#L44)

../../share/test.sol#L36-L51


 - [ ] ID-5
[CryptoRoulette.kill()](../../share/test.sol#L53-L57) uses timestamp for comparisons
	Dangerous comparisons:
	- [msg.sender == ownerAddr && now > lastPlayed + 86400](../../share/test.sol#L54)

../../share/test.sol#L53-L57


## deprecated-standards
Impact: Informational
Confidence: High
 - [ ] ID-6
Deprecated standard detected [secretNumber = uint8(sha3()(now,block.blockhash(block.number - 1))) % 20 + 1](../../share/test.sol#L33):
	- Usage of "block.blockhash()" should be replaced with "blockhash()"
	- Usage of "sha3()" should be replaced with "keccak256()"

../../share/test.sol#L33


 - [ ] ID-7
Deprecated standard detected [suicide(address)(msg.sender)](../../share/test.sol#L55):
	- Usage of "suicide()" should be replaced with "selfdestruct()"

../../share/test.sol#L55


## solc-version
Impact: Informational
Confidence: High
 - [ ] ID-8
Version constraint ^0.4.19 contains known severe issues (https://solidity.readthedocs.io/en/latest/bugs.html)
	- DirtyBytesArrayToStorage
	- ABIDecodeTwoDimensionalArrayMemory
	- KeccakCaching
	- EmptyByteArrayCopy
	- DynamicArrayCleanup
	- ImplicitConstructorCallvalueCheck
	- TupleAssignmentMultiStackSlotComponents
	- MemoryArrayCreationOverflow
	- privateCanBeOverridden
	- SignedArrayStorageCopy
	- ABIEncoderV2StorageArrayWithMultiSlotElement
	- DynamicConstructorArgumentsClippedABIV2
	- UninitializedFunctionPointerInConstructor_0.4.x
	- IncorrectEventSignatureInLibraries_0.4.x
	- ABIEncoderV2PackedStorage_0.4.x
	- ExpExponentCleanup
	- EventStructWrongData
	- NestedArrayFunctionCallDecoder.
It is used by:
	- [^0.4.19](../../share/test.sol#L4)

../../share/test.sol#L4


 - [ ] ID-9
solc-0.4.19 is an outdated solc version. Use a more recent version (at least 0.8.0), if possible.

## reentrancy-unlimited-gas
Impact: Informational
Confidence: Medium
 - [ ] ID-10
Reentrancy in [CryptoRoulette.play(uint256)](../../share/test.sol#L36-L51):
	External calls:
	- [msg.sender.transfer(this.balance)](../../share/test.sol#L46)
	State variables written after the call(s):
	- [lastPlayed = now](../../share/test.sol#L50)
	- [shuffle()](../../share/test.sol#L49)
		- [secretNumber = uint8(sha3()(now,block.blockhash(block.number - 1))) % 20 + 1](../../share/test.sol#L33)

../../share/test.sol#L36-L51


## constable-states
Impact: Optimization
Confidence: High
 - [ ] ID-11
[CryptoRoulette.betPrice](../../share/test.sol#L17) should be constant 

../../share/test.sol#L17


