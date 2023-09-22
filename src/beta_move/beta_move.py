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
        self._board: Moonboard = board
        self.allHolds: np.ndarray = np.zeros((1, 1))
        self.totalNumOfHold: int = 0
        # the index values of unused holds.
        self.holdsNotUsed: list[int] = []
        # index of holds used, in order of use.
        self.handSequence: list[int] = []
        # values of RH or LH to indicate which hand makes each move.
        self.handOperator: list[str] = []
        self.isFinished: bool = False
        self.touchEndHold = 0

    def match_hold_features(self: T, climb: Climb) -> np.ndarray:
        """
        Create an array of hold information.

        Parameters
        ----------
        climb : Climb
            The move order index of the first hold

        Returns
        -------
        numpy.ndarray
            A table of hold characteristics, locations, and start/end flags
        """
        x_vectors = np.zeros((10, climb.num_holds()))
        if climb.is_valid():
            i = 0
            holds = climb.get_holds()
            for (x, y) in holds:
                x_vectors[0:6, i] = self._board.get_features((x, y))
                x_vectors[6:8, i] = [x, y]
                i += 1
            x_vectors[8:, 0:climb.num_starts()] = np.array([[1], [0]])
            num_non_end = climb.num_holds() - climb.num_finish()
            x_vectors[8:, num_non_end:] = np.array([[0], [1]])
        else:
            raise Exception("Climb is invalid.")
        return x_vectors

    def create_movement(self: T, climb: Climb) -> dict:
        # movement = []
        x_vectors = self.match_hold_features(climb)
        self.allHolds = x_vectors.T
        self.totalNumOfHold = np.size(x_vectors.T, axis=0)
        self.holdsNotUsed.extend(range(self.totalNumOfHold))
        self.add_start_holds(0)

        # Run the algorithm for 6 times
        total_run = self.totalNumOfHold - 1
        for i in range(total_run):  # how many new move you wan to add
            if self.isFinished:
                break

        # produce output
        output = {}

        output["hold_index"] = self.handSequence
        output["hands"] = self.handOperator
        output["success"] = self.overall_success_rate()
        return output

    def add_start_holds(self: T, zero_or_one: int) -> None:
        """
        Specifically add the first two hold as the starting hold. Consider one
        hold start situation
        """
        op_list = ["LH", "RH"]
        start_hold_list = self.get_start_hold()
        first_start = start_hold_list[0]
        if len(start_hold_list) == 1:
            # Add a new hold into beta!
            first_order = self.get_order_from_hold(first_start)
            self.handSequence.append(int(first_order))
            self.handSequence.append(int(first_order))
            self.handOperator.extend(op_list)
            # Not consider match
            hold_order = self.get_order_from_hold(start_hold_list[0])
            self.holdsNotUsed.remove(hold_order)
        if len(start_hold_list) == 2:
            # Add a new hold into beta!
            second_start = start_hold_list[1]
            first_order = self.get_order_from_hold(first_start)
            second_order = self.get_order_from_hold(second_start)
            self.handSequence.append(int(first_order))
            self.handSequence.append(int(second_order))
            self.handOperator.append(op_list[zero_or_one])
            # indicate which hand
            self.handOperator.append(op_list[1 - zero_or_one])
            # Not consider match
            self.holdsNotUsed.remove(self.get_order_from_hold(first_start))
            self.holdsNotUsed.remove(self.get_order_from_hold(second_start))

    def get_all_holds(self: T) -> np.ndarray:
        """ return all avalible holds. N holds rows, 10 columns np array"""
        return self.allHolds

    def add_next_hand(self: T, next_hold: int, op: str) -> None:
        """
        Operation to make add the next hold. Append handsequence and hand
        operation. nextHold is a hold. op is "LH" or "RH"
        the last few lines don't really do anything.
        """
        if self.touchEndHold == 3:
            self.handSequence.append(self.totalNumOfHold - 1)
            if self.handSequence[-1] == "LH":
                self.handOperator.append("RH")
            if self.handSequence[-1] == "RH":
                self.handOperator.append("LH")
            self.touchEndHold = self.touchEndHold + 1
            self.isFinished = True

        elif self.touchEndHold == 1 or self.isFinished:
            pass
        else:
            if next_hold in self.get_end_hold_order():
                self.touchEndHold = self.touchEndHold + 1

            # Before Update a new hold

            # Update a new hold
            self.handSequence.append(next_hold)   # Add a new hold into beta!
            self.handOperator.append(op)         # indicate which hand
            if next_hold not in self.get_end_hold_order():
                self.holdsNotUsed.remove(next_hold)   # Not consider match

    def get_xy_from_order(self: T, hold_order: int) -> tuple:
        """
        return a coordinate tuple giving holdOrder
        (a num in processed data)
        """
        return ((self.allHolds[hold_order][6]), (self.allHolds[hold_order][7]))

    def get_left_hand_order(self: T) -> int:
        """
        Return a num of the last left hand hold's oreder
        (in processed data from bottom to top)
        """
        last_index_of_right = ''.join(self.handOperator).rindex('L') / 2
        return self.handSequence[int(last_index_of_right)]

    def get_right_hand_order(self: T) -> int:
        """
        Return a num of the last right hand hold's oreder
        (in processed data from bottom to top)
        """
        last_index_of_right = ''.join(self.handOperator).rindex('R') / 2
        return self.handSequence[int(last_index_of_right)]

    def get_left_hand_hold(self: T) -> np.ndarray:
        """
        Return a np array of the last right hand hold
        (in processed data from bottom to top)
        """
        return self.allHolds[self.get_left_hand_order()]

    def get_right_hand_hold(self: T) -> np.ndarray:
        """
        Return a np array of the last right hand hold
        (in processed data from bottom to top)
        """
        return self.allHolds[self.get_right_hand_order()]

    def get_order_from_hold(self: T, hold: np.ndarray) -> int:
        """
        from a single hold (np array) to an order
        """
        # Use np.where to get row indices
        indicies = np.where((self.allHolds == hold).all(1))
        return indicies[0][0]

    def get_com(self: T, hold1order: int, hold2order: int) -> tuple:
        """
        Get the coordinate of COM using current both hands order

        Parameters
        ----------
        hold1order : int
            The move order index of the first hold
        hold2order : int
            The move order index of the second hold

        Returns
        -------
        (float, float)
            The climber's center of mass coordinates
        """
        all_holds = self.allHolds
        x_com = (all_holds[hold1order][6] + all_holds[hold2order][6]) / 2
        y_com = (all_holds[hold1order][7] + all_holds[hold2order][7]) / 2
        return (x_com, y_com)

    def get_current_com(self: T) -> tuple:
        """
        Get the coordinate of center of mass based on current hand position
        """
        left = self.get_left_hand_order()
        right = self.get_right_hand_order()
        return self.get_com(left, right)

    def get_two_order_distance(self: T, remaining: int, next: int) -> float:
        """
        Given order 2, and 5. Output distance between
        remaining - Remaining Hand Order
        next - nextHoldOrder
        """
        original_com = self.get_current_com()
        final_com = self.get_com(remaining, next)
        com_0_dif_sq = (original_com[0] - final_com[0]) ** 2
        com_1_dif_sq = (original_com[1] - final_com[1]) ** 2
        return np.sqrt(com_0_dif_sq + com_1_dif_sq)

    def order_to_seq_order(self: T, order: int) -> int:
        """
        Transform from order (in the all avalible holds sequence) to hand
        order (in the hand sequence)
        """
        return self.handSequence.index(order)

    def last_move_success_rate_by_hold(self: T) -> int:
        left_hand_order = self.get_left_hand_order()
        left_seq_order = self.order_to_seq_order(left_hand_order)
        right_hand_order = self.get_right_hand_order()
        right_seq_order = self.order_to_seq_order(right_hand_order)

        operator_left = self.handOperator[left_seq_order]
        operator_right = self.handOperator[right_seq_order]
        left_hand_hold = self.get_left_hand_hold()
        right_hand_hold = self.get_right_hand_hold()
        left_success = self.success_rate_by_hold(left_hand_hold, operator_left)
        right_success = self.success_rate_by_hold(
            right_hand_hold, operator_right
        )
        return left_success * right_success

    def success_rate_by_hold(self: T, hold: np.ndarray, operation: str) -> int:
        """
        Evaluate the difficulty to hold on a hold applying LH or RH (op)
        """
        if operation == "LH":
            # Chiang's evaluation
            return self._board.get_lh_difficulty((hold[6], hold[7]))

            # Duh's evaluation
            # return max((hold[0] + 2 * hold[1] + hold[2] + hold[5]) **1.2,
            # (hold[2] / 2 + hold[3] + hold[4])) / hyperparameter[1]

        # if RH
        # Chiang's evaluation
        return self._board.get_rh_difficulty((hold[6], hold[7]))
        # return max((hold[2] + 2 * hold[3] + hold[4] + hold[5]) **1.2,
        # (hold[0] + hold[1] + hold[2] / 2)) / hyperparameter[1]

    def get_start_hold(self: T) -> list:
        """return startHold list with 2 element of np array"""
        start_holds = []
        for hold in self.allHolds:
            if hold[8] == 1:
                start_holds.append(hold)
        return start_holds

    def get_end_hold_order(self: T) -> list:
        """return endHold list with 2 element of np array"""
        end_hold_order = []
        for i in range(self.totalNumOfHold):
            if self.allHolds[i][9] == 1:
                end_hold_order.append(i)
        if len(end_hold_order) == 1:
            end_hold_order.append(self.totalNumOfHold)
        return end_hold_order

    def overall_success_rate(self: T) -> float:
        """
        return the overall successful rate using the stored beta hand sequence
        """
        num_of_hand = len(self.handSequence)
        overall_score = 1.0
        for i, order in enumerate(self.handSequence):
            hold_index = self.allHolds[order]
            hand_operator = self.handOperator[i]
            overall_score *= self.success_rate_by_hold(
                hold_index, hand_operator
            )

        for i in range(num_of_hand - 1):
            # Penalty of do a big cross. Larger will drop the successRate
            target_xy = self.get_xy_from_order(self.handSequence[i+1])

            # update last L/R hand
            last_hand_xy = self.get_xy_from_order(self.handSequence[i])
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
                gaussian = self.make_gaussian(target_xy, center, "LH")
                overall_score = overall_score * gaussian
            if i >= 1 and self.handOperator[i + 1] == "LH":
                original_xy = last_right_hand_xy
                center = (original_xy[0], original_xy[1])
                gaussian = self.make_gaussian(target_xy, center, "RH")
                overall_score = overall_score * gaussian
        self.overallSuccess = overall_score

        return overall_score ** (3 / num_of_hand)

    def set_true_beta(self: T) -> None:
        self.isTrueBeta = True

    def get_holds_not_used(self: T) -> list:
        return self.holdsNotUsed

    def add_new_beta(self: T, print_out: bool = True) -> list:
        """
        Add one move to expand the candidate list and pick the largest 8
        """
        tempstatus = []
        distance_score = []
        hyperparameter = [1, 1]
        for next_hold_order in self.holdsNotUsed:
            original_com = self.get_current_com()
            hyper_0 = hyperparameter[0]
            dynamic_threshold = hyper_0 * self.last_move_success_rate_by_hold()
            final_xy = self.get_xy_from_order(next_hold_order)
            dif_x = original_com[0] - final_xy[0]
            dif_y = original_com[1] - final_xy[1]
            distance = np.sqrt(dif_x ** 2 + dif_y ** 2)
            # evaluate success rate simply consider the distance
            # (not consider left and right hand)
            success = self.success_rate_by_distance(
                distance,
                dynamic_threshold
            )
            distance_score.append(success)

        # Find the first and second smallest distance in the distance_score
        num = min(8, len(distance_score))
        iter = range(len(distance_score))
        key_name = distance_score.__getitem__
        largest_index = heapq.nlargest(num, iter, key=key_name)

        good_hold_index = [self.holdsNotUsed[i] for i in largest_index]
        added = False
        for possible_hold in good_hold_index:
            for op in ["RH", "LH"]:
                if not self.isFinished:
                    tempstatus.append(copy.deepcopy(self))
                    tempstatus[-1].add_next_hand(possible_hold, op)
                elif not added:
                    tempstatus.append(copy.deepcopy(self))
                    added = True

        # trim tempstatus to pick the largest 8
        final_score = []
        final_score.append(self.overall_success_rate())
        iter = range(len(final_score))
        largest_index = heapq.nlargest(8, iter, key=final_score.__getitem__)
        return [tempstatus[i] for i in largest_index]

    @classmethod
    def make_gaussian(
        cls: Type[T],
        target: tuple,
        center: tuple,
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
            guess1 = cls.gauss(target, (x0 - 3, y0 + 1.5), fwhm)
            guess2 = cls.gauss(target, (x0 + 1, y0 + .5), fwhm) * .4

            # thirdGauss =  np.exp(
            # -4*np.log(2) * ((x-(x0))**2 + (y-(y0+1))**2) / fwhm**2) * 0.3
        if lasthand == "LH":
            guess1 = cls.gauss(target, (x0 + 3, y0 + 1.5), fwhm)
            guess2 = cls.gauss(target, (x0 - 1, y0 + .5), fwhm) * .4

            # thirdGauss =  np.exp(
            # -4*np.log(2) * ((x-(x0))**2 + (y-(y0+1))**2) / fwhm**2) * 0.3
        return guess1 + guess2

    @classmethod
    def gauss(cls: Type[T], target: tuple, center: tuple, fwhm: int) -> float:
        x = target[0]
        y = target[1]
        x0 = center[0]
        y0 = center[1]
        return np.exp(
            -4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2
        )

    @classmethod
    def success_rate_by_distance(
        cls: Type[T], distance: float, dynamic_threshold: float
    ) -> float:
        """ Relu funtion to get the successrate """
        ratio = 1 - distance / dynamic_threshold
        return 0 if distance >= dynamic_threshold else ratio
