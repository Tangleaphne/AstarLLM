// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

// 单个Collection合约
contract NFTCollection is ERC721URIStorage, Ownable, ReentrancyGuard {
    using Strings for uint256;
    
    uint256 private _tokenIds;
    uint256 public maxSupply;
    uint256 public currentSupply;
    uint256 public mintPrice;
    string public baseTokenURI;
    bool public isActive = true;
    
    // 每日铸造限制
    uint256 public dailyMintLimit = 10;
    mapping(address => uint256) public dailyMints;
    mapping(address => uint256) public lastMintDay;
    
    // NFT市场相关
    mapping(uint256 => uint256) public tokenIdToPrice;
    mapping(uint256 => bool) public isTokenListed;
    uint256 public platformFee = 25; // 2.5%
    
    // 事件
    event NFTMinted(uint256 indexed tokenId, address minter);
    event NFTListed(uint256 indexed tokenId, uint256 price, address seller);
    event NFTSold(uint256 indexed tokenId, uint256 price, address seller, address buyer);
    event NFTUnlisted(uint256 indexed tokenId);
    
    constructor(
        string memory name,
        string memory symbol,
        uint256 _maxSupply,
        string memory _baseTokenURI,
        uint256 _mintPrice,
        address creator
    ) ERC721(name, symbol) Ownable(creator) ReentrancyGuard() {
        maxSupply = _maxSupply;
        baseTokenURI = _baseTokenURI;
        mintPrice = _mintPrice;
    }
    
    // 检查并重置每日铸造限制
    modifier checkDailyLimit() {
        uint256 currentDay = block.timestamp / 86400;
        if (currentDay > lastMintDay[msg.sender]) {
            dailyMints[msg.sender] = 0;
            lastMintDay[msg.sender] = currentDay;
        }
        require(dailyMints[msg.sender] < dailyMintLimit, "Daily mint limit reached");
        _;
    }

    function totalSupply() public view returns (uint256) {
        return currentSupply;
    }
    
    // 添加设置 baseURI 的函数
    function setBaseURI(string memory _baseURI) public onlyOwner {
        baseTokenURI = _baseURI;
    }
    
    function mint() public payable checkDailyLimit returns (uint256) {
        require(isActive, "Collection is not active");
        require(msg.value >= mintPrice, "Insufficient payment");
        
        if(maxSupply > 0) {
            require(currentSupply < maxSupply, "Supply limit reached");
        }
        
        _tokenIds++;
        uint256 newTokenId = _tokenIds;
        
        _safeMint(msg.sender, newTokenId);
        
        // 现在 baseTokenURI 应该是元数据的 IPFS hash
        // 构建完整的 tokenURI
        string memory tokenURI = string(abi.encodePacked("ipfs://", baseTokenURI));
        _setTokenURI(newTokenId, tokenURI);
        
        currentSupply++;
        dailyMints[msg.sender]++;
        
        emit NFTMinted(newTokenId, msg.sender);
        return newTokenId;
    }
    
    
    // NFT市场相关函数
    function listNFT(uint256 tokenId, uint256 price) public {
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        require(price > 0, "Price must be positive");
        
        tokenIdToPrice[tokenId] = price;
        isTokenListed[tokenId] = true;
        
        emit NFTListed(tokenId, price, msg.sender);
    }
    
    function buyNFT(uint256 tokenId) public payable nonReentrant {
        require(isTokenListed[tokenId], "Token not listed");
        uint256 price = tokenIdToPrice[tokenId];
        require(msg.value >= price, "Insufficient payment");
        
        address seller = ownerOf(tokenId);
        require(seller != msg.sender, "Cannot buy your own token");
        
        uint256 fee = (price * platformFee) / 1000;
        uint256 sellerAmount = price - fee;
        
        _transfer(seller, msg.sender, tokenId);
        payable(seller).transfer(sellerAmount);
        
        isTokenListed[tokenId] = false;
        delete tokenIdToPrice[tokenId];
        
        emit NFTSold(tokenId, price, seller, msg.sender);
    }
    
    function unlistNFT(uint256 tokenId) public {
        require(ownerOf(tokenId) == msg.sender, "Not token owner");
        require(isTokenListed[tokenId], "Token not listed");
        
        isTokenListed[tokenId] = false;
        delete tokenIdToPrice[tokenId];
        
        emit NFTUnlisted(tokenId);
    }
    
    // 管理函数
    function toggleActive() public onlyOwner {
        isActive = !isActive;
    }
    
    function setMintPrice(uint256 _mintPrice) public onlyOwner {
        mintPrice = _mintPrice;
    }
    
    function setPlatformFee(uint256 _fee) public onlyOwner {
        require(_fee <= 100, "Fee too high"); // 最高10%
        platformFee = _fee;
    }
    
    function setDailyMintLimit(uint256 _limit) public onlyOwner {
        dailyMintLimit = _limit;
    }
    
    function withdraw() public onlyOwner {
        uint256 balance = address(this).balance;
        payable(owner()).transfer(balance);
    }
}

// Collection工厂合约
contract NFTCollectionFactory is Ownable {
    // 结构体定义，用于存储合约地址和名称
    struct CollectionInfo {
        address collectionAddress;
        string name;
    }

    // 记录已创建的 Collection 信息
    CollectionInfo[] public collections;

    // 记录已创建的collection
    //address[] public collections;
    mapping(address => bool) public isCollection;
    //mapping(address => string) public collectionNames;
    
    event CollectionCreated(address indexed collection, address indexed creator, string name);
    
    constructor() Ownable(msg.sender) {}
    
    function createCollection(
        string memory name,
        string memory symbol,
        uint256 maxSupply,
        string memory baseTokenURI,
        uint256 mintPrice
    ) public returns (address) {
        require(bytes(name).length > 0, "Name cannot be empty");
        require(bytes(symbol).length > 0, "Symbol cannot be empty");

        NFTCollection newCollection = new NFTCollection(
            name,
            symbol,
            maxSupply,
            baseTokenURI,
            mintPrice,
            msg.sender
        );
        
        //collections.push(address(newCollection));
        // 将合约地址和名称存入 collections 数组
        collections.push(CollectionInfo({
            collectionAddress: address(newCollection),
            name: name
        }));
        isCollection[address(newCollection)] = true;
    
        emit CollectionCreated(address(newCollection), msg.sender, name);
        return address(newCollection);
    }
    
    function getCollectionAddressesAndNames() public view returns (address[] memory, string[] memory) {
        uint256 length = collections.length;
        address[] memory addresses = new address[](length);
        string[] memory names = new string[](length);

        for (uint256 i = 0; i < length; i++) {
            addresses[i] = collections[i].collectionAddress;
            names[i] = collections[i].name;
        }

        return (addresses, names);
    }

    function getCollections() public view returns (CollectionInfo[] memory) {
        return collections;
    }

    //function getCollectionName(address collection) public view returns (string memory) {
    //        return collectionNames[collection];
    //    }
}