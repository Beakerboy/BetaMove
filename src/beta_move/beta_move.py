import copy
import heapq
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
        self.allHolds = []
        self.totalNumOfHold = 0
        self.holdsNotUsed = []
        self.handSequence = []
        self.handOperator = []
        self.isFinished = False

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
            self.allHolds = x_vectors.T
            self.totalNumOfHold = np.size(x_vectors.T, axis=0)
            self.holdsNotUsed.extend(range(self.totalNumOfHold))
            self.addStartHolds(0)

            # Run the algorithm for 6 times
            totalRun = self.totalNumOfHold - 1
            for i in range(totalRun):  # how many new move you wan to add
                status = self.addNewBeta()
                finalScore = self.overallSuccessRate()
                largestIndex = heapq.nlargest(4, range(len(finalScore)), key=finalScore.__getitem__)
                if self.isFinished:
                    break
    
            # last sorting for the best 5
            finalScore = self.overallSuccessRate() 
            largestIndex = heapq.nlargest(1, range(len(finalScore)), key=finalScore.__getitem__)
            # produce output
            output = {}
            
            output["hand_sequence"] = self.handSequence
            output["hand_operator"] = self.handOperator
            output["success"] = self.overallSuccessRate()
            return output

    def addStartHolds(self: T, zeroOrOne):
        """
        Specifically add the first two hold as the starting hold. Consider one
        hold start situation
        """
        opList = ["LH", "RH"]
        startHoldList = self.getStartHold()
        first_start = startHoldList[0]
        if len(startHoldList) == 1:
            # Add a new hold into beta!
            self.handSequence.append(int(self.getOrderFromHold(first_start)))
            self.handSequence.append(int(self.getOrderFromHold(first_start)))
            self.handOperator.extend(opList)
            # Not consider match
            self.holdsNotUsed.remove(self.getOrderFromHold(startHoldList[0]))
        if len(startHoldList) == 2:
            # Add a new hold into beta!
            second_start = startHoldList[1]
            self.handSequence.append(int(self.getOrderFromHold(first_start)))
            self.handSequence.append(int(self.getOrderFromHold(second_start)))
            self.handOperator.append(opList[zeroOrOne])
            # indicate which hand
            self.handOperator.append(opList[1 - zeroOrOne])
            # Not consider match
            self.holdsNotUsed.remove(self.getOrderFromHold(first_start))
            self.holdsNotUsed.remove(self.getOrderFromHold(second_start))

    def getAllHolds(self: T):
        """ return all avalible holds. N holds rows, 10 columns np array"""
        return self.allHolds

    def addNextHand(self: T, nextHold, op):
        """
        Operation to make add the next hold. Append handsequence and hand
        operation. nextHold is a hold. op is "LH" or "RH"
        """  
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
            hyper_zero = hyperparameter[0]
            dynamicThreshold = hyper_zero * self.lastMoveSuccessRateByHold()  
 
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
            com_0_dif_sq = (originalCom[0] - finalCom[0]) ** 2
            com_1_dif_sq = (originalCom[1] - finalCom[1]) ** 2
            distance = np.sqrt(com_0_dif_sq + com_1_dif_sq)

    def getXYFromOrder(self: T, holdOrder):
        """
        return a coordinate tuple giving holdOrder (a num in processed data)
        """
        return ((self.allHolds[holdOrder][6]), (self.allHolds[holdOrder][7])) 

    def getleftHandOrder(self: T):
        """
        Return a num of the last left hand hold's oreder (in processed data from bottom to top)
        """
        lastIndexOfRight = ''.join(self.handOperator).rindex('R') / 2
        return self.handSequence[int(lastIndexOfRight)]

    def getrightHandOrder(self: T):
        """
        Return a num of the last right hand hold's oreder (in processed data from bottom to top)
        """
        lastIndexOfRight = ''.join(self.handOperator).rindex('R') / 2
        return self.handSequence[int(lastIndexOfRight)]

    def getleftHandHold(self: T):
        """
        Return a np array of the last right hand hold (in processed data from bottom to top)
        """
        return self.allHolds[self.getleftHandOrder()]

    def getrightHandHold(self: T):
        """
        Return a np array of the last right hand hold (in processed data from bottom to top)
        """
        return self.allHolds[self.getrightHandOrder()]

    def getOrderFromHold(self: T, hold):
        """
        from a single hold (np array) to an order
        """
        # Use np.where to get row indices
        return np.where((self.allHolds == hold).all(1))[0]

    def getCom(self: T, hold1Order: int, hold2Order: int)-> tuple:
        """
        Get the coordinate of COM using current both hands order

        Parameters
        ----------
        hold1Order : int
            The move order index of the first hold
        hold2Order : int
            The move order index of the second hold

        Returns
        -------
        (float, float)
            The climber's center of mass coordinates
        """
        all_holds = self.allHolds
        xCom = (all_holds[hold1Order][6] + all_holds[hold2Order][6]) / 2
        yCom = (all_holds[hold1Order][7] + all_holds[hold2Order][7]) / 2
        return (xCom, yCom)

    def getCurrentCom(self: T) -> tuple:
        """
        Get the coordinate of center of mass based on current hand position
        """
        return self.getCom(self.getleftHandOrder(), self.getrightHandOrder())

    def getTwoOrderDistance(self: T, remaining, next) -> float:
        """
        Given order 2, and 5. Output distance between
        remaining - Remaining Hand Order
        next - nextHoldOrder
        """
        originalCom = self.getCurrentCom()
        finalCom = self.getCom(remaining, next)
        com_0_dif_sq = (originalCom[0] - finalCom[0]) ** 2
        com_1_dif_sq = (originalCom[1] - finalCom[1]) ** 2
        return np.sqrt(com_0_dif_sq + com_1_dif_sq)

    def orderToSeqOrder(self: T, order):
        """
        Transform from order (in the all avalible holds sequence) to hand
        order (in the hand sequence)
        """
        return self.handSequence.index(order)

    def lastMoveSuccessRateByHold(self: T) -> int:
        left_hand_order = self.getleftHandOrder()
        left_seq_order = self.orderToSeqOrder(left_hand_order)
        right_hand_order = self.getrightHandOrder()
        right_seq_order = self.orderToSeqOrder(right_hand_order)

        operator_left = self.handOperator[left_seq_order]
        operator_right = self.handOperator[right_seq_order]
        left_hand_hold = self.getleftHandHold()
        right_hand_hold = self.getrightHandHold()
        left_success = self.successRateByHold(left_hand_hold, operator_left)
        right_success = self.successRateByHold(right_hand_hold, operator_right)
        return left_success * right_success

    def successRateByHold(self: T, hold: list, operation: str) -> int:
        """
        Evaluate the difficulty to hold on a hold applying LH or RH (op)
        """
        if operation == "LH":
            # Chiang's evaluation
            return self._board.get_lh_difficulty((hold[6], hold[7]))

            # Duh's evaluation
            # return max((hold[0] + 2 * hold[1] + hold[2] + hold[5]) **1.2,
            # (hold[2] / 2 + hold[3] + hold[4])) / hyperparameter[1]
        if operation == "RH":
            # Chiang's evaluation
            return self._board.get_rh_difficulty((hold[6], hold[7]))
            # return max((hold[2] + 2 * hold[3] + hold[4] + hold[5]) **1.2,
            # (hold[0] + hold[1] + hold[2] / 2)) / hyperparameter[1]

    def getStartHold(self: T) -> list:
        """return startHold list with 2 element of np array"""
        start_holds = []
        for hold in self.allHolds:
            if hold[8] == 1:
                start_holds.append(hold)
        return start_holds

    def getEndHoldOrder(self: T) -> list:
        """return endHold list with 2 element of np array"""
        end_hold_order = []
        for i in range(self.totalNumOfHold):
            if self.allHolds[i][9] == 1:
                end_hold_order.append(i)
        if len(end_hold_order) == 1:
            end_hold_order.append(self.totalNumOfHold)
        return end_hold_order

    def overallSuccessRate(self: T) -> float:
        """
        return the overall successful rate using the stored beta hand sequence
        """
        num_of_hand = len(self.handSequence)
        overall_score = 1
        for i, order in enumerate(self.handSequence):
            hold_index = self.allHolds[order]
            hand_operator = self.handOperator[i]
            overall_score *= self.successRateByHold(hold_index, hand_operator)

        for i in range(num_of_hand - 1):
            # Penalty of do a big cross. Larger will drop the successRate
            target_xy = self.getXYFromOrder(self.handSequence[i+1])

            # update last L/R hand
            last_hand_xy = self.getXYFromOrder(self.handSequence[i])
            if self.handOperator[i] == "RH":
                last_right_hand_xy = last_hand_xy
            if self.handOperator[i] == "LH":
                last_left_hand_xy = last_hand_xy

            if i == 1 and self.handSequence[0] == self.handSequence[1]:
                # not sure
                target_xy = (target_xy[0], target_xy[1] - 1)

            if i >= 1 and self.handOperator[i + 1] == "RH":
                original_xy = last_left_hand_xy
                center = (original_xy[0], original_xy[1])
                overall_score *= self.make_gaussian(target_xy, center, "LH")
            if i >= 1 and self.handOperator[i + 1] == "LH":
                original_xy = last_right_hand_xy
                center = (original_xy[0], original_xy[1])
                overall_score *= self.make_gaussian(target_xy, center, "RH")
        self.overallSuccess = overall_score

        return overall_score ** (3 / num_of_hand)

    def setTrueBeta(self: T) -> bool:
        self.isTrueBeta = True

    def getholdsNotUsed(self: T) -> list:
        return self.holdsNotUsed

    def addNewBeta(self: T, printOut = True):
        """
        Add one move to expand the candidate list and pick the largest 8
        """
        tempstatus = []   
        distanceScore = []
        hyperparameter = [1, 1]
        for nextHoldOrder in self.holdsNotUsed:
            originalCom = self.getCurrentCom() 
            dynamicThreshold = hyperparameter[0] * self.lastMoveSuccessRateByHold()  
            finalXY = self.getXYFromOrder(nextHoldOrder)
            distance = np.sqrt(((originalCom[0] - finalXY[0]) ** 2)+((originalCom[1] - finalXY[1]) ** 2))
            # evaluate success rate simply consider the distance (not consider left and right hand)
            distanceScore.append(self.successRateByDistance(distance, dynamicThreshold))

        # Find the first and second smallest distance in the distanceScore
        largestIndex = heapq.nlargest(min(8, len(distanceScore)), range(len(distanceScore)), key=distanceScore.__getitem__)
    
        # goodHoldIndex = [betaPre.holdsNotUsed[largestIndex[0]], betaPre.holdsNotUsed[largestIndex[1]], betaPre.holdsNotUsed[largestIndex[2]]]  #[#3,#5] holds
        goodHoldIndex = [self.holdsNotUsed[i] for i in largestIndex]
        added = False
        for possibleHold in goodHoldIndex:
            for op in ["RH", "LH"]:
                if self.isFinished == False:
                    tempstatus.append(copy.deepcopy(self))
                    tempstatus[-1].addNextHand(possibleHold, op)
                elif added == False:
                    tempstatus.append(copy.deepcopy(self))
                    added = True

        # trim tempstatus to pick the largest 8
        finalScore = []       
        for i in tempstatus:
            finalScore.append(i.overallSuccessRate())    
        largestIndex = heapq.nlargest(8, range(len(finalScore)), key=finalScore.__getitem__) 
        return [tempstatus[i] for i in largestIndex]

    @classmethod
    def make_gaussian(
        cls: Type[T],
        target: list,
        center: list,
        lasthand: str = "LH"
    ) -> float:
        """ Make a square gaussian filter to evaluate how possible of the
        relative distance between hands from target hand to remaining hand
        (center)
        fwhm is full-width-half-maximum, which can be thought of as an
        effective distance of dynamic range.
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

    def successRateByDistance(cls: Type[T], distance, dynamicThreshold):
        """ Relu funtion to get the successrate """
        if distance < dynamicThreshold:
            return 1 - distance / dynamicThreshold
        if distance >= dynamicThreshold:
            return 0
