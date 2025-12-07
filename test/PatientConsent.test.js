const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("PatientConsentNFT", function () {
    let consentContract;
    let owner;
    let addr1;

    beforeEach(async function () {
        [owner, addr1] = await ethers.getSigners();
        const PatientConsent = await ethers.getContractFactory("PatientConsentNFT");
        consentContract = await PatientConsent.deploy();
    });

    it("Should mint a new NFT to the patient", async function () {
        const tx = await consentContract.mintConsentNFT(addr1.address, "P01", "QmHash...");
        await tx.wait();
        expect(await consentContract.ownerOf(1)).to.equal(addr1.address);
    });

    it("Should allow owner to update consent", async function () {
        await consentContract.mintConsentNFT(addr1.address, "P01", "QmHash...");

        // Switch to addr1 (patient)
        const patientContract = consentContract.connect(addr1);
        await patientContract.updateConsent(1, true, 0);

        const details = await patientContract.getConsentDetails(1);
        expect(details.allowTraining).to.equal(true);
    });
});
