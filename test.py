def shouldBurstIn(playerHealth, timeWaited, acceptableLoss, acceptableTime):
    shouldBurst = False
    healthLoss = (100.0 - playerHealth)/100
    if healthLoss < acceptableLoss or timeWaited > acceptableTime :
        shouldBurst = True
        timeWaited = 0
    else :
        timeWaited += 1
    
    return shouldBurst, timeWaited