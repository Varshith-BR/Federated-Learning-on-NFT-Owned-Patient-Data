// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title PatientConsentNFT
 * @dev Implements a decentralized consent management system using NFTs.
 * Each patient's data ownership is represented by a unique NFT.
 * The metadata of the NFT controls the consent settings for Federated Learning.
 */
contract PatientConsentNFT is ERC721, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    struct ConsentData {
        string patientId;
        string dataHash;     // IPFS or local hash of the medical record
        bool allowTraining;  // True: Data can be used for FL
        uint256 expiryDate;  // Timestamp when consent expires (0 = never)
        uint256 lastUpdated; // Timestamp of last update
    }

    // Map Token ID to Consent Data
    mapping(uint256 => ConsentData) public consents;
    
    // Map Patient Internal ID to Token ID (for reverse lookup)
    mapping(string => uint256) public patientTokenMap;

    event ConsentUpdated(uint256 indexed tokenId, string patientId, bool allowTraining, uint256 expiryDate);
    event PatientRegistered(uint256 indexed tokenId, string patientId, address wallet);

    constructor() ERC721("PatientDataConsent", "PDC") {}

    /**
     * @dev Mints a new Consent NFT for a patient.
     * @param to The wallet address of the patient.
     * @param patientId The internal hospital ID of the patient.
     * @param dataHash Cryptographic hash of the patient's dataset.
     */
    function mintConsentNFT(address to, string memory patientId, string memory dataHash) public onlyOwner returns (uint256) {
        _tokenIds.increment();
        uint256 newItemId = _tokenIds.current();

        _mint(to, newItemId);

        consents[newItemId] = ConsentData({
            patientId: patientId,
            dataHash: dataHash,
            allowTraining: false, // Default to NO consent
            expiryDate: 0,
            lastUpdated: block.timestamp
        });

        patientTokenMap[patientId] = newItemId;

        emit PatientRegistered(newItemId, patientId, to);
        return newItemId;
    }

    /**
     * @dev Updates the consent status. Only the NFT owner (patient) can call this.
     * @param tokenId The ID of the NFT.
     * @param allowTraining Boolean flag for consent.
     * @param expiryDate Unix timestamp for expiration (optional).
     */
    function updateConsent(uint256 tokenId, bool allowTraining, uint256 expiryDate) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "Caller is not owner nor approved");

        ConsentData storage data = consents[tokenId];
        data.allowTraining = allowTraining;
        data.expiryDate = expiryDate;
        data.lastUpdated = block.timestamp;

        emit ConsentUpdated(tokenId, data.patientId, allowTraining, expiryDate);
    }

    /**
     * @dev View function called by the Federated Learning Server to check permission.
     * @param tokenId The ID of the patient's NFT.
     * @return bool True if training is allowed and not expired.
     */
    function isConsentValid(uint256 tokenId) public view returns (bool) {
        ConsentData memory data = consents[tokenId];

        if (!data.allowTraining) {
            return false;
        }

        if (data.expiryDate > 0 && block.timestamp > data.expiryDate) {
            return false;
        }

        return true;
    }

    /**
     * @dev Returns full metadata for a patient.
     */
    function getConsentDetails(uint256 tokenId) public view returns (ConsentData memory) {
        return consents[tokenId];
    }
}
