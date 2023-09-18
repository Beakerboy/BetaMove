import numpy as np
from beta_move.climb import Climb
from beta_move.moonboard import Moonboard
from typing import TypeVar, Type


T = TypeVar('T', bound='BetaMove')


class BetaMove:

    # class default constructor
    def __init__(self: T, board: Moonboard) -> None:

        # Instance Attributes
        self._board = board

    def create_movement(self: T, climb: Climb) -> list:
        # movement = []
        if climb.is_valid:
            i = 0
            x_vectors = np.zeros((10, climb.num_holds()))
            holds = climb.get_holds()
            for (x, y) in holds:
                x_vectors[0:6, i] = self._board.get_features((x, y))
                x_vectors[6:8, i] = [x, y]
                i += 1
            x_vectors[8:, 0:climb.num_starts()] = np.array([[1], [0]])
            num_non_end = climb.num_holds() - climb.num_finish()
            x_vectors[8:, num_non_end:] = np.array([[0], [1]])

        return x_vectors

    def addStartHolds(self: T, zeroOrOne):
        """ Specifically add the first two hold as the starting hold. Consider one hold start situation"""
        opList = ["LH", "RH"]
        startHoldList = self.getStartHold()
        if len(startHoldList) == 1:
            self.handSequence.append(int(self.getOrderFromHold(startHoldList[0])))   # Add a new hold into beta!
            self.handSequence.append(int(self.getOrderFromHold(startHoldList[0])))
            self.handOperator.extend(opList) 
            self.holdsNotUsed.remove(self.getOrderFromHold(startHoldList[0]))   # Not consider match
        if len(startHoldList) == 2:  
            self.handSequence.append(int(self.getOrderFromHold(startHoldList[0])))   # Add a new hold into beta!
            self.handSequence.append(int(self.getOrderFromHold(startHoldList[1])))
            self.handOperator.append(opList[zeroOrOne]) 
            self.handOperator.append(opList[1-zeroOrOne]) # indicate which hand
            self.holdsNotUsed.remove(self.getOrderFromHold(startHoldList[0]))   # Not consider match
            self.holdsNotUsed.remove(self.getOrderFromHold(startHoldList[1]))
            
    def getAllHolds(self: T):
        """ return all avalible holds. N holds rows, 10 columns np array"""
        return self.allHolds
    
    def addNextHand(self: T, nextHold, op):
        """ Operation to make add the next hold. Append handsequence and hand operation. nextHold is a hold. op is "LH" or "RH" """     
        hyperparameter = [1, 1]
        if self.touchEndHold == 3: 
            self.handSequence.append(self.totalNumOfHold - 1)  
            if self.handSequence[-1] == "LH":
                self.handOperator.append("RH")  
            if self.handSequence[-1] == "RH":
                self.handOperator.append("LH") 
            self.touchEndHold = self.touchEndHold + 1;
            self.isFinished = True

        elif self.touchEndHold == 1 or self.isFinished == True: 
            pass
        else:
            if nextHold in self.getEndHoldOrder():
                self.touchEndHold = self.touchEndHold + 1;
                
            # Before Update a new hold
            originalCom = self.getCurrentCom()
            dynamicThreshold = hyperparameter[0] * self.lastMoveSuccessRateByHold()  
 
            # Update a new hold
            self.handSequence.append(nextHold)   # Add a new hold into beta!
            self.handOperator.append(op)         # indicate which hand
            if nextHold not in self.getEndHoldOrder():
                self.holdsNotUsed.remove(nextHold)   # Not consider match
            
            # after add a new hold
            if op == "LH":
                remainingHandOrder = self.getrightHandOrder()
            else:
                remainingHandOrder = self.getleftHandOrder()
            
            finalCom = self.getCom(remainingHandOrder, nextHold)
            distance = np.sqrt(((originalCom[0] - finalCom[0]) ** 2)+((originalCom[1] - finalCom[1]) ** 2))

    def getXYFromOrder(self: T, holdOrder):
        """return a coordinate tuple giving holdOrder (a num in processed data)"""
        return ((self.allHolds[holdOrder][6]), (self.allHolds[holdOrder][7])) 
    
    def getleftHandOrder(self: T):
        """ Return a num of the last left hand hold's oreder (in processed data from bottom to top)"""
        lastIndexOfRight = ''.join(self.handOperator).rindex('R') / 2
        return self.handSequence[int(lastIndexOfRight)]
    
    def getrightHandOrder(self: T):
        """ Return a num of the last right hand hold's oreder (in processed data from bottom to top)"""
        lastIndexOfRight = ''.join(self.handOperator).rindex('R') / 2
        return self.handSequence[int(lastIndexOfRight)]

    def getleftHandHold(self: T):
        """ Return a np array of the last right hand hold (in processed data from bottom to top)"""
        return self.allHolds[self.getleftHandOrder()]
    
    def getrightHandHold(self: T):
        """ Return a np array of the last right hand hold (in processed data from bottom to top)"""
        return self.allHolds[self.getrightHandOrder()]
    
    def getOrderFromHold(self: T, hold):
        """ from a single hold (np array) to an order"""
        return np.where((self.allHolds == hold).all(1))[0] # Use np.where to get row indices
    
    def getCom(self: T, hold1Order, hold2Order)-> tuple:
        """ Get the coordinate of COM using current both hands order"""
        xCom = (self.allHolds[hold1Order][6] + self.allHolds[hold2Order][6]) / 2
        yCom = (self.allHolds[hold1Order][7] + self.allHolds[hold2Order][7]) / 2
        return (xCom, yCom)

        
    def getCurrentCom(self: T) -> tuple:
        """ Get the coordinate of COM based on current hand position"""
        return self.getCom(self.getleftHandOrder(), self.getrightHandOrder())
    
    def getTwoOrderDistance(self: T, remainingHandOrder, nextHoldOrder) -> float:
        """ Given order 2, and 5. Output distance between"""
        originalCom = self.getCurrentCom()
        finalCom = self.getCom(remainingHandOrder, nextHoldOrder)
        return np.sqrt(((originalCom[0] - finalCom[0]) ** 2)+((originalCom[1] - finalCom[1]) ** 2))

    def orderToSeqOrder(self: T, order):
        """ Transform from order (in the all avalible holds sequence) to hand order (in the hand sequence)"""
        return self.handSequence.index(order)
    
    def lastMoveSuccessRateByHold(self: T):
        operatorLeft = self.handOperator[self.orderToSeqOrder(self.getleftHandOrder())]
        operatorRight = self.handOperator[self.orderToSeqOrder(self.getrightHandOrder())]
        return self.successRateByHold(self.getleftHandHold(), operatorLeft) * self.successRateByHold(self.getrightHandHold(), operatorRight)
    
    def successRateByHold(self: T, hold, operation) -> int:
        """ Evaluate the difficulty to hold on a hold applying LH or RH (op)"""
        if operation == "LH": 
            return self._board.get_lh_difficulty((hold[6], hold[7])) #Chiang's evaluation
            # Duh's evaluation
            # return max((hold[0] + 2 * hold[1] + hold[2] + hold[5]) **1.2  , (hold[2] / 2 + hold[3] + hold[4])) / hyperparameter[1]  
        if operation == "RH":
            return self._board.get_rh_difficulty((hold[6], hold[7])) #Chiang's evaluation
            # return max((hold[2] + 2 * hold[3] + hold[4] + hold[5]) **1.2 , (hold[0] + hold[1] + hold[2] / 2)) / hyperparameter[1]
        
    def getStartHold(self: T) -> list:
        """return startHold list with 2 element of np array"""
        startHoldList = []
        for hold in self.allHolds:
            if hold[8] == 1:
                startHoldList.append(hold)
        return startHoldList

    def getEndHoldOrder(self: T) -> list:
        """return endHold list with 2 element of np array"""
        endHoldOrderList = []
        for i in range(self.totalNumOfHold):
            if self.allHolds[i][9] == 1:
                endHoldOrderList.append(i)
        if len(endHoldOrderList) == 1:
            endHoldOrderList.append(self.totalNumOfHold)
        return endHoldOrderList
    
    def overallSuccessRate(self: T) -> float:
        """
        return the overall successful rate using the stored beta hand sequence
        """
        numOfHand = len(self.handSequence)
        overallScore = 1;
        for i, order in enumerate(self.handSequence): 
            overallScore = overallScore * self.successRateByHold(self.allHolds[order], self.handOperator[i])
  
        for i in range(numOfHand - 1):
            # Penalty of do a big cross. Larger will drop the successRate   
            target_xy = self.getXYFromOrder(self.handSequence[i+1]) 
            
            # update last L/R hand
            if self.handOperator[i] == "RH":
                lastrightHandXY = self.getXYFromOrder(self.handSequence[i]) 
            if self.handOperator[i] == "LH":
                lastleftHandXY = self.getXYFromOrder(self.handSequence[i])
                
            if i == 1 and self.handSequence[0] == self.handSequence[1]:
                # not sure
                target_xy = (target_xy[0], target_xy[1] - 1)
            
            if i >= 1 and self.handOperator[i+1] == "RH": 
                original_xy = lastleftHandXY
                center = (original_xy[0], original_xy[1])
                overallScore *= self.make_gaussian(target_xy, center, "LH")
            if i >= 1 and self.handOperator[i+1] == "LH": 
                original_xy = lastrightHandXY
                center = (original_xy[0], original_xy[1])
                overallScore *= self.make_gaussian(target_xy, center, "RH")
        self.overallSuccess = overallScore
        
        return overallScore ** (3 / numOfHand)
    
    def setTrueBeta(self: T) -> bool:
        self.isTrueBeta = True

    def getholdsNotUsed(self: T) -> list:
        return self.holdsNotUsed

    @classmethod
    def make_gaussian(cls: Type[T],
                      target: list,
                      center: list,
                      lasthand: str = "LH"
                     ) -> float:
        """ Make a square gaussian filter to evaluate how possible of the
        relative distance between hands from target hand to remaining hand
        (center)
        fwhm is full-width-half-maximum, which can be thought of as an effective
        distance of dynamic range.
        """
        fwhm = 3
        x0 = center[0]
        y0 = center[1]
        if lasthand == "RH":
            guess1 = cls.gauss(target, [x0 - 3, y0 + 1.5], fwhm)
            guess2 = cls.gauss(target, [x0 + 1, y0 + .5], fwhm) * .4

            # thirdGauss =  np.exp(
            # -4*np.log(2) * ((x-(x0))**2 + (y-(y0+1))**2) / fwhm**2) * 0.3
        if lasthand == "LH":
            guess1 = cls.gauss(target, [x0 + 3, y0 + 1.5], fwhm)
            guess2 = cls.gauss(target, [x0 - 1, y0 + .5], fwhm) * .4

            # thirdGauss =  np.exp(
            # -4*np.log(2) * ((x-(x0))**2 + (y-(y0+1))**2) / fwhm**2) * 0.3
        return guess1 + guess2

    @classmethod
    def gauss(cls: Type[T], target: list, center: list, fwhm: int) -> float:
        x = target[0]
        y = target[1]
        x0 = center[0]
        y0 = center[1]
        return np.exp(
            -4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2
        )
