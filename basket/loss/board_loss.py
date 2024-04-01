from basket.loss.basic_loss import BasicLoss
from basket.utils.maths import *


class BoardLoss(BasicLoss):
    def __init__(self, env, sim,
                 dis_typ: str,
                 coeff_interval: float,
                 coeff_late: float,
                 coeff_ground: float,
                 coeff_dir: float,
                 coeff_board: float):
        super().__init__(env, sim, dis_typ,
                         coeff_interval, coeff_late,
                         coeff_ground, coeff_dir)

        self.coeff_board = coeff_board

        self.loss_funcs = [self.get_loss_1,
                           self.get_loss_2,
                           self.get_loss_3,
                           self.get_loss_4]

    def get_loss_1(self):
        loss = None

        pos_list, vel_list = self.sim.pos_list, self.sim.vel_list
        target_pos = self.env.target_pos
        target_x, target_y = target_pos[0], target_pos[1]

        def update_loss(i):
            nonlocal loss
            t = (target_x - pos_list[i][0]) / vel_list[i][0]
            actual_y = pos_list[i][1] + vel_list[i][1] * t
            delta_y = actual_y - target_y
            if self.dis_typ == 'L1':
                tmp_loss = calc_abs(delta_y)
            else:
                tmp_loss = calc_sq(delta_y)
            if vel_list[i][1].val > 0:
                tmp_loss -= vel_list[i][1] * self.coeff_dir
            if loss is None or tmp_loss.val < loss.val:
                loss = tmp_loss

        for i in range(len(pos_list) - 1):
            tup_x = pos_list[i][0].val, pos_list[i + 1][0].val
            if min(*tup_x) < target_x <= max(*tup_x):
                update_loss(i)

        if loss is None:
            idx = None
            for i in range(len(pos_list)):
                if vel_list[i][0].val <= 0:
                    continue
                if idx is None or pos_list[i][0].val > pos_list[idx][0].val:
                    idx = i
            assert idx is not None
            update_loss(idx)

        assert isinstance(loss, Scalar)
        print('loss1:', loss)
        return loss

    def get_loss_3(self):
        # Obtenir la perte pour basket.y < self.env.ground_threshold
        loss = Scalar(0)
        pos_list = self.sim.pos_list
        for i in range(min(int(self.sim.tap_times[-1] / self.sim.dt), len(pos_list))):
            height = pos_list[i][1] - self.env.ground_threshold
            if height.val < 0:
                if self.dis_typ == 'L1':
                    tmp_loss = calc_abs(height)
                else:
                    tmp_loss = calc_sq(height)
                if tmp_loss.val > loss.val:
                    loss = tmp_loss
        loss *= self.coeff_ground
        print('loss3:', loss)
        return loss

    def get_loss_4(self):
        if self.sim.collide_board_id:
            return Scalar(0)

        pos_list, vel_list = self.sim.pos_list, self.sim.vel_list

        board_x = self.env.target_pos[0] + self.env.basket_radius + \
            self.env.basket_ring_radius
        board_y_lb = self.env.target_pos[1]
        board_y_ub = self.env.target_pos[1] + self.env.board_height

        idx = None
        for i in range(len(pos_list)):
            if vel_list[i][0].val <= 0:
                break
            if pos_list[i][0].val < board_x:
                idx = i

        t = (board_x - pos_list[idx][0]) / vel_list[idx][0]
        actual_y = pos_list[idx][1] + vel_list[idx][1] * t

        if actual_y < board_y_lb:
            loss = board_y_lb - actual_y
        elif actual_y > board_y_ub:
            loss = actual_y - board_y_ub
        else:
            loss = Scalar(0)

        assert isinstance(loss, Scalar)
        print('loss4:', loss * self.coeff_board)
        return loss * self.coeff_board
