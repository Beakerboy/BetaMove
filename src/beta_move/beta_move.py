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

    # Getters and Setters
    def get_holds_not_used(self: T) -> list:
        """
        Returns
        -------
        list[int]
            a list of the index values in allHolds which have not been used.
        """
        return self.holdsNotUsed

    def get_all_holds(self: T) -> np.ndarray:
        """
        Returns
        -------
        numpy.ndarray
            A table of hold characteristics, locations, and start/end flags
        """
        return self.allHolds

    def get_start_hold(self: T) -> list:
        start_holds = []
        for hold in self.allHolds:
            if hold[8] == 1:
                start_holds.append(hold)
        return start_holds

    def match_hold_features(self: T, climb: Climb) -> np.ndarray:
        """
        Create an array of hold information.

        Parameters
        ----------
        climb : Climb
            The holds available in the problem.

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

    def create_movement(self: T, climb: Climb) -> T:
        # movement = []
        x_vectors = self.match_hold_features(climb)
        self.allHolds = x_vectors.T
        self.totalNumOfHold = np.size(x_vectors.T, axis=0)
        self.holdsNotUsed = list(range(self.totalNumOfHold))
        beta1 = copy.deepcopy(self)
        beta2 = copy.deepcopy(self)
        status = [beta1, beta2]
        status[0].add_start_holds(False)
        status[1].add_start_holds(True)
        total_run = status[0].totalNumOfHold - 1

        for i in range(total_run):
            status = BetaMove.add_new_beta(status, False)
            final_score = []
            for j in status:
                final_score.append(j.overall_success_rate())
                iter = range(len(final_score))
                key_func = final_score.__getitem__
                largest_index = heapq.nlargest(4, iter, key=key_func)
                comp1 = status[largest_index[0]].isFinished
                if comp1 and status[largest_index[1]].isFinished:
                    break
        final_score = []
        for j in status:
            final_score.append(j.overall_success_rate())
        iter = range(len(final_score))
        key_func = final_score.__getitem__
        largest_index = heapq.nlargest(1, iter, key=key_func)
        return status[largest_index[0]]

    def process_data(self: T, climb: Climb) -> np.ndarray:
        movement = self.create_movement(climb)
        output = np.vstack([
            self.allHolds.T[6:8, movement.handSequence],
            ((np.array(movement.handOperator) == 'LH') * (-1)
             + (np.array(movement.handOperator) == 'RH') * 1),
            # missing code for the last line
        ])
        return output

    def generate_hand_string_sequence(self: T, climb: Climb) -> list:
        movement = self.create_movement(climb)
        result = []
        for i, index in enumerate(movement.handSequence):
            xy = movement.get_xy_from_order(index)
            location = Moonboard.coordinate_to_string(xy)
            movement_string = location + '-' + movement.handOperator[i]
            result.append(movement_string)
        return result

    def add_start_holds(self: T, right_first: bool) -> None:
        """
        Add the start hold(s) to the beta lists. If there is one hold, list
        it twice, and move both hands to it. If there are two, use the
        parameter to determine which hand is assigned to which start hold.

        Parameters
        ----------
        right_first : boolean
            Is the right hand or left hand first?

        Returns
        -------
        numpy.ndarray
            A table of hold characteristics, locations, and start/end flags
        """
        op_list = ["LH", "RH"]
        start_hold_list = self.get_start_hold()
        first_start = start_hold_list[0]
        if len(start_hold_list) == 1:
            # Add a new hold into beta.
            first_order = self.get_order_from_hold(first_start)
            self.handSequence.append(int(first_order))
            self.handSequence.append(int(first_order))
            self.handOperator.extend(op_list)

            hold_order = self.get_order_from_hold(start_hold_list[0])
            self.holdsNotUsed.remove(hold_order)
        if len(start_hold_list) == 2:
            # Add a new hold into beta.
            second_start = start_hold_list[1]
            first_order = self.get_order_from_hold(first_start)
            second_order = self.get_order_from_hold(second_start)
            self.handSequence.append(int(first_order))
            self.handSequence.append(int(second_order))
            # Set the specified hand to each hold.
            zero_or_one = 1 if right_first else 0
            self.handOperator.append(op_list[zero_or_one])
            self.handOperator.append(op_list[1 - zero_or_one])
            self.holdsNotUsed.remove(self.get_order_from_hold(first_start))
            self.holdsNotUsed.remove(self.get_order_from_hold(second_start))

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
            else:
                self.holdsNotUsed.remove(next_hold)   # Not consider match
            # Update a new hold
            self.handSequence.append(next_hold)   # Add a new hold into beta!
            self.handOperator.append(op)         # indicate which hand

    def get_xy_from_order(self: T, hold_order: int) -> tuple:
        """
        return a coordinate tuple giving holdOrder
        (a num in processed data)
        """
        x = int(self.allHolds[hold_order][6])
        y = int(self.allHolds[hold_order][7])
        return (x, y)

    def get_left_hand_order(self: T) -> int:
        """
        Return a num of the last left hand hold's order index
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

    def order_to_seq_order(self: T, order: int) -> int:
        """
        Transform from order (in the all avalible holds sequence) to hand
        order (in the hand sequence)
        """
        return self.handSequence.index(order)

    def last_move_success_rate_by_hold(self: T) -> int:
        left_hand_hold = self.get_left_hand_hold()
        right_hand_hold = self.get_right_hand_hold()
        left_success = self.success_rate_by_hold(left_hand_hold, "LH")
        right_success = self.success_rate_by_hold(right_hand_hold, "RH")
        return left_success * right_success

    def success_rate_by_hold(self: T, hold: np.ndarray, operation: str) -> int:
        """
        Evaluate the difficulty to hold on a hold applying LH or RH (op)
        """
        if operation == "LH":
            return self._board.get_lh_difficulty((hold[6], hold[7]))
        return self._board.get_rh_difficulty((hold[6], hold[7]))

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
            hold = self.allHolds[order]
            hand_operator = self.handOperator[i]
            success = self.success_rate_by_hold(hold, hand_operator)
            overall_score *= success

        for i in range(num_of_hand - 1):
            # Penalty of do a big cross. Larger will drop the successRate
            target_xy = self.get_xy_from_order(self.handSequence[i+1])

            if self.handOperator[i] == "RH":
                tmp = self.get_xy_from_order(self.handSequence[i])
                last_right_hand_xy = tmp
            if self.handOperator[i] == "LH":
                tmp = self.get_xy_from_order(self.handSequence[i])
                last_left_hand_xy = tmp

            if i == 1 and self.handSequence[0] == self.handSequence[1]:
                # this move was to match the start.
                # not sure why adjusting the target.
                target_xy = (target_xy[0], target_xy[1] - 1)

            if i >= 1 and self.handOperator[i + 1] == "RH":
                last_hand = last_left_hand_xy
                gaussian = self.make_gaussian(target_xy, last_hand, "LH")
                overall_score = overall_score * gaussian

            elif i >= 1 and self.handOperator[i + 1] == "LH":
                last_hand = last_right_hand_xy
                gaussian = self.make_gaussian(target_xy, last_hand, "RH")
                overall_score = overall_score * gaussian
        self.overallSuccess = overall_score

        return overall_score ** (3 / num_of_hand)

    def set_true_beta(self: T) -> None:
        self.isTrueBeta = True

    @classmethod
    def add_new_beta(cls: Type[T],
                     status: list,
                     print_out: bool = True
                     ) -> list:
        """
        Add one move to expand the candidate list and pick the largest 8
        """
        tempstatus = []
        for beta_pre in status:
            distance_scores = []
            hyperparameter = [1, 1]
            for next_hold_order in beta_pre.holdsNotUsed:
                original_com = np.array(beta_pre.get_current_com())
                hyper_0 = hyperparameter[0]
                success_rate = beta_pre.last_move_success_rate_by_hold()
                dynamic_threshold = hyper_0 * success_rate
                final_coor = beta_pre.get_xy_from_order(next_hold_order)
                final_xy = np.array(final_coor)
                distance = np.linalg.norm(original_com - final_xy)
                # evaluate success rate simply consider the distance
                # (not consider left and right hand)
                success = beta_pre.success_rate_by_distance(
                    distance,
                    dynamic_threshold
                )
                distance_scores.append(success)
            # Find the first and second smallest distance in the distance_score
            num = min(8, len(distance_scores))
            iter = range(len(distance_scores))
            key_name = distance_scores.__getitem__
            largest_index = heapq.nlargest(num, iter, key=key_name)

            good_hold_index = [beta_pre.holdsNotUsed[i] for i in largest_index]
            added = False
            for possible_hold in good_hold_index:
                for op in ["RH", "LH"]:
                    if not beta_pre.isFinished:
                        tempstatus.append(copy.deepcopy(beta_pre))
                        tempstatus[-1].add_next_hand(possible_hold, op)
                    elif not added:
                        tempstatus.append(copy.deepcopy(beta_pre))
                        added = True

        # trim tempstatus to pick the largest 8
        final_score = []
        for i in tempstatus:
            final_score.append(i.overall_success_rate())
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

    @classmethod
    def coordinate_to_string(cls: Type[T], coordinate: tuple) -> str:
        """ convert (9.0 ,4.0) to "J5" """
        alphabet_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
        str1 = alphabet_list[int(coordinate[0])]
        return str(str1) + str(int(coordinate[1]) + 1)
