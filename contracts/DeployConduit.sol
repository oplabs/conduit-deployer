// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import {ConduitControllerInterface} from "./ConduitControllerInterface.sol";

contract DeployConduit {
    constructor(address owner) {
        address me = address(this);
        bytes32 conduitKey = bytes32(abi.encodePacked(me, bytes24(0)));
        ConduitControllerInterface controller = ConduitControllerInterface(
            0x00000000F9490004C11Cef243f5400493c00Ad63
        );

        // Deploy the conduit
        address conduit = controller.createConduit(conduitKey, me);

        // Open Seaport channel
        controller.updateChannel(
            conduit,
            0x00000000000001ad428e4906aE43D8F9852d0dD6,
            true
        );

        // Transfer ownership
        controller.transferOwnership(conduit, owner);
    }
}
