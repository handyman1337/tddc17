import math

class StateAndReward:
    """State discretization and reward helpers for the Q-learning controller."""

    @staticmethod
    def get_state_angle(angle, vx, vy):
        """State discretization function for the angle controller."""
        # Exercise 1a: Discretize the angle and return a unique state.

        #TUNE THIS IF NEEDED
        NR_OF_ANGLE_STATES = 10 #360/10 = 36 deg per discrete angle
        MAX_ANGLE = math.pi #We use radians since simulator printed radians
        
        state = StateAndReward.discretize2(
            angle,
            NR_OF_ANGLE_STATES,
            -MAX_ANGLE,
            MAX_ANGLE)

        return state

    @staticmethod
    def get_reward_angle(angle, vx, vy):
        """Reward function for the angle controller."""

        # Exercise 1b: Return a reward that favors an upright rocket.

        reward = 1 - abs(angle) / math.pi

        return reward

    @staticmethod
    def get_state_hover(angle, vx, vy):
        """State discretization function for the full hover controller."""

        # Exercise 4a: Build a state from angle, vx, and vy.
        #TUNE THESE IF NEEDED
        NR_OF_ANGLE_STATES = 10 #360/10 = 36 deg per discrete angle
        NR_OF_VX_STATES = 5 #left / kinda still / right
        NR_OF_VY_STATES = 5 #heavy up / up / kinda still / down / heavy down
        MAX_ANGLE = math.pi #We use radians since simulator printed radians
        MAX_VX = 35.0
        MAX_VY = 35.0 
        
        angle_bin = StateAndReward.discretize2(
            angle, NR_OF_ANGLE_STATES, -MAX_ANGLE, MAX_ANGLE)
        
        #discretize() used instead of discretize2() here because we want under-/overflow bins for velocity
        vx_bin = StateAndReward.discretize(
            vx, NR_OF_VX_STATES, -MAX_VX, MAX_VX)
        
        vy_bin = StateAndReward.discretize(
            vy, NR_OF_VY_STATES, -MAX_VY, MAX_VY)
    
        state = (angle_bin, vx_bin, vy_bin)

        return state

    @staticmethod
    def get_reward_hover(angle, vx, vy):
        """Reward function for the full hover controller."""
        #SET THESE TO THE SAME AS THE ABOVE METHOD
        MAX_VX = 35.0
        MAX_VY = 35.0

        # Exercise 4b: Return a reward for hovering.
        reward_ang = 1 - abs(angle) / math.pi
        reward_vx = max(0.0, 1 - abs(vx) / MAX_VX)
        reward_vy = max(0.0, 1 - abs(vy) / MAX_VY)
        
        return (reward_ang + reward_vx + reward_vy) 

    @staticmethod
    def discretize(value, nr_values, min_value, max_value):
        """Uniform discretization with explicit underflow and overflow bins.

        Returns an integer between 0 and nr_values - 1.

        If value is lower than min_value, 0 is returned. If value is higher
        than max_value, nr_values - 1 is returned. Otherwise a value between
        1 and nr_values - 2 is returned.
        """
        if nr_values < 2:
            return 0

        diff = max_value - min_value

        if value < min_value:
            return 0
        if value > max_value:
            return nr_values - 1

        temp_value = value - min_value
        ratio = temp_value / diff

        return int(ratio * (nr_values - 2)) + 1

    @staticmethod
    def discretize2(value, nr_values, min_value, max_value):
        """Uniform discretization without separate inner edge bins.

        Returns an integer between 0 and nr_values - 1.
        """
        diff = max_value - min_value

        if value < min_value:
            return 0
        if value > max_value:
            return nr_values - 1

        temp_value = value - min_value
        ratio = temp_value / diff

        return int(ratio * nr_values)
