const hre = require("hardhat");

async function main() {
    const currentTimestampInSeconds = Math.round(Date.now() / 1000);
    const ONE_YEAR_IN_SECS = 365 * 24 * 60 * 60;
    const unlockTime = currentTimestampInSeconds + ONE_YEAR_IN_SECS;

    console.log("Deploying PatientConsentNFT contract...");

    const PatientConsent = await hre.ethers.getContractFactory("PatientConsentNFT");
    const consentContract = await PatientConsent.deploy();

    await consentContract.deployed();

    console.log(
        `PatientConsentNFT deployed to: ${consentContract.address}`
    );

    console.log("Verifying contract on Etherscan...");
    // Verification logic would go here
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
