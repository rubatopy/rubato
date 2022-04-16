"""
A utility for generating simple smooth noise in your projects.
"""
from . import Math


class Noise:
    """
    A modified implementation of the OpenSimplex2 algorithm.

    Attributes:
        seed (int): The seed for the random noise. Setting to a fixed value will result in the same noise every time.
    """
    seed = 0

    _PRIME_X = 0x5205402B9270C86F
    _PRIME_Y = 0x598CD327003817B5
    _PRIME_Z = 0x5BCC226E9FA0BACB
    _PRIME_W = 0x56CC5227E58F554B
    _HASH_MULTIPLIER = 0x53A3F72DEEC546F5
    _SEED_FLIP_3D = -0x52D547B2E96ED629
    _SEED_OFFSET_4D = 0xE83DC3E0DA7164D

    _ROOT2OVER2 = 0.7071067811865476
    _SKEW_2D = 0.366025403784439
    _UNSKEW_2D = -0.21132486540518713

    _ROOT3OVER3 = 0.577350269189626
    _FALLBACK_ROTATE_3D = 2.0 / 3.0
    _ROTATE_3D_ORTHOGONALIZER = _UNSKEW_2D

    _SKEW_4D = -0.138196601125011
    _UNSKEW_4D = 0.309016994374947
    _LATTICE_STEP_4D = 0.2

    _N_GRADS_2D_EXPONENT = 7
    _N_GRADS_3D_EXPONENT = 8
    _N_GRADS_4D_EXPONENT = 9
    _N_GRADS_2D = 1 << _N_GRADS_2D_EXPONENT
    _N_GRADS_3D = 1 << _N_GRADS_3D_EXPONENT
    _N_GRADS_4D = 1 << _N_GRADS_4D_EXPONENT

    _NORMALIZER_2D = 0.01001634121365712
    _NORMALIZER_3D = 0.07969837668935331
    _NORMALIZER_4D = 0.0220065933241897

    _RSQUARED_2D = 0.5
    _RSQUARED_3D = 0.6
    _RSQUARED_4D = 0.6

    _GRADIENTS_2D = []
    _GRADIENTS_3D = []
    _GRADIENTS_4D = []

    @classmethod
    def noise(cls, x: float) -> float:
        """
        Creates noise from 1 dimensional input.
        This is identical to :func:`noise2(x, 0) <rubato.utils.noise.Noise.noise2>`.

        Args:
            x (float): the x coordinate of noise.

        Returns:
            float: the random noise value.
        """
        return cls.noise2(x, 0)

    @classmethod
    def noise2(cls, x: float, y: float) -> float:
        """
        Creates noise from 2 dimensional input.

        Args:
            x (float): the x coordinate of noise.
            y (float): the y coordinate of noise.

        Returns:
            float: the random noise value.
        """
        s = cls._SKEW_2D * (x + y)
        xs = x + s
        ys = y + s

        return cls._noise2_base(cls.seed, xs, ys)

    @classmethod
    def noise3(cls, x: float, y: float, z: float) -> float:
        """
        Creates noise from 3 dimensional input.

        Args:
            x (float): the x coordinate of noise.
            y (float): the y coordinate of noise.
            z (float): the z coordinate of noise.

        Returns:
            float: the random noise value.
        """
        r = cls._FALLBACK_ROTATE_3D * (x + y + z)
        xr = r - x
        yr = r - y
        zr = r - z

        return cls._noise3_base(cls.seed, xr, yr, zr)

    @classmethod
    def noise4(cls, x: float, y: float, z: float, w: float) -> float:
        """
        Creates noise from 4 dimensional input.

        Args:
            x (float): the x coordinate of noise.
            y (float): the y coordinate of noise.
            z (float): the z coordinate of noise.
            w (float): the w coordinate of noise.

        Returns:
            float: the random noise value.
        """
        s = cls._SKEW_4D * (x + y + z + w)
        xs = x + s
        ys = y + s
        zs = z + s
        ws = w + s

        return cls._noise4_base(cls.seed, xs, ys, zs, ws)

    @classmethod
    def _noise2_base(cls, seed: int, xs: float, ys: float) -> float:
        xsb = Math.floor(xs)
        ysb = Math.floor(ys)
        xi = xs - xsb
        yi = ys - ysb

        xsbp = xsb * cls._PRIME_X
        ysbp = ysb * cls._PRIME_Y

        t = (xi + yi) * cls._UNSKEW_2D
        dx0 = xi + t
        dy0 = yi + t

        value = 0
        a0 = cls._RSQUARED_2D - dx0 * dx0 - dy0 * dy0
        if a0 > 0:
            value = (a0 * a0) * (a0 * a0) * cls._grad2(seed, xsbp, ysbp, dx0, dy0)

        a1 = (2 * (1 + 2 * cls._UNSKEW_2D) *
              (1 / cls._UNSKEW_2D + 2)) * t + ((-2 * (1 + 2 * cls._UNSKEW_2D) * (1 + 2 * cls._UNSKEW_2D)) + a0)
        if a1 > 0:
            dx1 = dx0 - (1 + 2 * cls._UNSKEW_2D)
            dy1 = dy0 - (1 + 2 * cls._UNSKEW_2D)
            value += (a1 * a1) * (a1 * a1) * cls._grad2(seed, xsbp + cls._PRIME_X, ysbp + cls._PRIME_Y, dx1, dy1)

        if dy0 > dx0:
            dx2 = dx0 - cls._UNSKEW_2D
            dy2 = dy0 - (cls._UNSKEW_2D + 1)
            a2 = cls._RSQUARED_2D - dx2 * dx2 - dy2 * dy2
            if a2 > 0:
                value += (a2 * a2) * (a2 * a2) * cls._grad2(seed, xsbp, ysbp + cls._PRIME_Y, dx2, dy2)
        else:
            dx2 = dx0 - (cls._UNSKEW_2D + 1)
            dy2 = dy0 - cls._UNSKEW_2D
            a2 = cls._RSQUARED_2D - dx2 * dx2 - dy2 * dy2
            if a2 > 0:
                value += (a2 * a2) * (a2 * a2) * cls._grad2(seed, xsbp + cls._PRIME_X, ysbp, dx2, dy2)

        return value

    @classmethod
    def _grad2(cls, seed: int, xsvp: int, ysvp: int, dx: float, dy: float) -> float:
        hash_val = seed ^ xsvp ^ ysvp
        hash_val *= cls._HASH_MULTIPLIER
        hash_val ^= hash_val >> (64 - cls._N_GRADS_2D_EXPONENT + 1)
        gi = int(hash_val) & ((cls._N_GRADS_2D - 1) << 1)
        return cls._GRADIENTS_2D[gi | 0] * dx + cls._GRADIENTS_2D[gi | 1] * dy

    @classmethod
    def _noise3_base(cls, seed: int, xr: float, yr: float, zr: float) -> float:
        xrb = Math.round(xr)
        yrb = Math.round(yr)
        zrb = Math.round(zr)
        xri = xr - xrb
        yri = yr - yrb
        zri = zr - zrb

        x_n_sign = int(-1.0 - xri) | 1
        y_n_sign = int(-1.0 - yri) | 1
        z_n_sign = int(-1.0 - zri) | 1

        ax0 = x_n_sign * -xri
        ay0 = y_n_sign * -yri
        az0 = z_n_sign * -zri

        xrbp = xrb * cls._PRIME_X
        yrbp = yrb * cls._PRIME_Y
        zrbp = zrb * cls._PRIME_Z

        value = 0
        a = (cls._RSQUARED_3D - xri * xri) - (yri * yri + zri * zri)
        l = 0
        while True:
            if a > 0:
                value += (a * a) * (a * a) * cls._grad3(seed, xrbp, yrbp, zrbp, xri, yri, zri)

            if ax0 >= ay0 and ax0 >= az0:
                b = a + ax0 + ax0
                if b > 1:
                    b -= 1
                    value += (b * b) * (b * b) * cls._grad3(
                        seed, xrbp - x_n_sign * cls._PRIME_X, yrbp, zrbp, xri + x_n_sign, yri, zri
                    )
            elif ay0 > ax0 and ay0 >= az0:
                b = a + ay0 + ay0
                if b > 1:
                    b -= 1
                    value += (b * b) * (b * b) * cls._grad3(
                        seed, xrbp, yrbp - y_n_sign * cls._PRIME_Y, zrbp, xri, yri + y_n_sign, zri
                    )
            else:
                b = a + az0 + az0
                if b > 1:
                    b -= 1
                    value += (b * b) * (b * b) * cls._grad3(
                        seed, xrbp, yrbp, zrbp - z_n_sign * cls._PRIME_Z, xri, yri, zri + z_n_sign
                    )

            if l == 1:
                break

            ax0 = 0.5 - ax0
            ay0 = 0.5 - ay0
            az0 = 0.5 - az0

            xri = x_n_sign * ax0
            yri = y_n_sign * ay0
            zri = z_n_sign * az0

            a += (0.75 - ax0) - (ay0 + az0)

            xrbp += (x_n_sign >> 1) & cls._PRIME_X
            yrbp += (y_n_sign >> 1) & cls._PRIME_Y
            zrbp += (z_n_sign >> 1) & cls._PRIME_Z

            x_n_sign = -x_n_sign
            y_n_sign = -y_n_sign
            z_n_sign = -z_n_sign

            seed ^= cls._SEED_FLIP_3D

            l += 1

        return value

    @classmethod
    def _grad3(cls, seed: int, xrvp: int, yrvp: int, zrvp: int, dx: float, dy: float, dz: float) -> float:
        hash_val = (seed ^ xrvp) ^ (yrvp ^ zrvp)
        hash_val *= cls._HASH_MULTIPLIER
        hash_val ^= hash_val >> (64 - cls._N_GRADS_3D_EXPONENT + 2)
        gi = int(hash_val) & ((cls._N_GRADS_3D - 1) << 2)
        return cls._GRADIENTS_3D[gi | 0] * dx + cls._GRADIENTS_3D[gi | 1] * dy + cls._GRADIENTS_3D[gi | 2] * dz

    @classmethod
    def _noise4_base(cls, seed: int, xs: float, ys: float, zs: float, ws: float) -> float:
        xsb = Math.floor(xs)
        ysb = Math.floor(ys)
        zsb = Math.floor(zs)
        wsb = Math.floor(ws)
        xsi = xs - xsb
        ysi = ys - ysb
        zsi = zs - zsb
        wsi = ws - wsb

        si_sum = (xsi + ysi) + (zsi + wsi)
        starting_lattice = int(si_sum * 1.25)

        seed += starting_lattice * cls._SEED_OFFSET_4D

        starting_lattice_offset = starting_lattice * -cls._LATTICE_STEP_4D
        xsi += starting_lattice_offset
        ysi += starting_lattice_offset
        zsi += starting_lattice_offset
        wsi += starting_lattice_offset

        ssi = (si_sum + starting_lattice_offset * 4) * cls._UNSKEW_4D

        xsvp = xsb * cls._PRIME_X
        ysvp = ysb * cls._PRIME_Y
        zsvp = zsb * cls._PRIME_Z
        wsvp = wsb * cls._PRIME_W

        value = 0
        i = 0
        while True:
            score0 = 1.0 + ssi * (-1.0 / cls._UNSKEW_4D)
            if (xsi >= ysi and xsi >= zsi and xsi >= wsi and xsi >= score0):
                xsvp += cls._PRIME_X
                xsi -= 1
                ssi -= cls._UNSKEW_4D
            elif (ysi > xsi and ysi >= zsi and ysi >= wsi and ysi >= score0):
                ysvp += cls._PRIME_Y
                ysi -= 1
                ssi -= cls._UNSKEW_4D
            elif (zsi > xsi and zsi > ysi and zsi >= wsi and zsi >= score0):
                zsvp += cls._PRIME_Z
                zsi -= 1
                ssi -= cls._UNSKEW_4D
            elif (wsi > xsi and wsi > ysi and wsi > zsi and wsi >= score0):
                wsvp += cls._PRIME_W
                wsi -= 1
                ssi -= cls._UNSKEW_4D

            dx = xsi + ssi
            dy = ysi + ssi
            dz = zsi + ssi
            dw = wsi + ssi
            a = (dx * dx + dy * dy) + (dz * dz + dw * dw)
            if a < cls._RSQUARED_4D:
                a -= cls._RSQUARED_4D
                a *= a
                value += a * a * cls._grad4(seed, xsvp, ysvp, zsvp, wsvp, dx, dy, dz, dw)

            if i == 4:
                break

            xsi += cls._LATTICE_STEP_4D
            ysi += cls._LATTICE_STEP_4D
            zsi += cls._LATTICE_STEP_4D
            wsi += cls._LATTICE_STEP_4D
            ssi += cls._LATTICE_STEP_4D * 4 * cls._UNSKEW_4D
            seed -= cls._SEED_OFFSET_4D

            if i == starting_lattice:
                xsvp -= cls._PRIME_X
                ysvp -= cls._PRIME_Y
                zsvp -= cls._PRIME_Z
                wsvp -= cls._PRIME_W
                seed += cls._SEED_OFFSET_4D * 5

            i += 1

        return value

    @classmethod
    def _grad4(
        cls, seed: int, xsvp: int, ysvp: int, zsvp: int, wsvp: int, dx: float, dy: float, dz: float, dw: float
    ) -> float:
        hash_val = seed ^ (xsvp ^ ysvp) ^ (zsvp ^ wsvp)
        hash_val *= cls._HASH_MULTIPLIER
        hash_val ^= hash_val >> (64 - cls._N_GRADS_4D_EXPONENT + 2)
        gi = int(hash_val) & ((cls._N_GRADS_4D - 1) << 2)
        return (cls._GRADIENTS_4D[gi | 0] * dx +
                cls._GRADIENTS_4D[gi | 1] * dy) + (cls._GRADIENTS_4D[gi | 2] * dz + cls._GRADIENTS_4D[gi | 3] * dw)

    # below is the generator code for the gradients

    _gradient2 = [
        0.38268343236509,
        0.923879532511287,
        0.923879532511287,
        0.38268343236509,
        0.923879532511287,
        -0.38268343236509,
        0.38268343236509,
        -0.923879532511287,
        -0.38268343236509,
        -0.923879532511287,
        -0.923879532511287,
        -0.38268343236509,
        -0.923879532511287,
        0.38268343236509,
        -0.38268343236509,
        0.923879532511287,
        0.130526192220052,
        0.99144486137381,
        0.608761429008721,
        0.793353340291235,
        0.793353340291235,
        0.608761429008721,
        0.99144486137381,
        0.130526192220051,
        0.99144486137381,
        -0.130526192220051,
        0.793353340291235,
        -0.60876142900872,
        0.608761429008721,
        -0.793353340291235,
        0.130526192220052,
        -0.99144486137381,
        -0.130526192220052,
        -0.99144486137381,
        -0.608761429008721,
        -0.793353340291235,
        -0.793353340291235,
        -0.608761429008721,
        -0.99144486137381,
        -0.130526192220052,
        -0.99144486137381,
        0.130526192220051,
        -0.793353340291235,
        0.608761429008721,
        -0.608761429008721,
        0.793353340291235,
        -0.130526192220052,
        0.99144486137381,
    ]

    for _gradient_i in range(len(_gradient2)):
        _gradient2[_gradient_i] = _gradient2[_gradient_i] / _NORMALIZER_2D

    _gradient_j = 0
    for _gradient_i in range(_N_GRADS_2D * 2):
        if _gradient_j == len(_gradient2):
            _gradient_j = 0
        _GRADIENTS_2D.append(_gradient2[_gradient_j])
        _gradient_j += 1

    _gradient3 = [
        2.22474487139,
        2.22474487139,
        -1.0,
        0.0,
        2.22474487139,
        2.22474487139,
        1.0,
        0.0,
        3.0862664687972017,
        1.1721513422464978,
        0.0,
        0.0,
        1.1721513422464978,
        3.0862664687972017,
        0.0,
        0.0,
        -2.22474487139,
        2.22474487139,
        -1.0,
        0.0,
        -2.22474487139,
        2.22474487139,
        1.0,
        0.0,
        -1.1721513422464978,
        3.0862664687972017,
        0.0,
        0.0,
        -3.0862664687972017,
        1.1721513422464978,
        0.0,
        0.0,
        -1.0,
        -2.22474487139,
        -2.22474487139,
        0.0,
        1.0,
        -2.22474487139,
        -2.22474487139,
        0.0,
        0.0,
        -3.0862664687972017,
        -1.1721513422464978,
        0.0,
        0.0,
        -1.1721513422464978,
        -3.0862664687972017,
        0.0,
        -1.0,
        -2.22474487139,
        2.22474487139,
        0.0,
        1.0,
        -2.22474487139,
        2.22474487139,
        0.0,
        0.0,
        -1.1721513422464978,
        3.0862664687972017,
        0.0,
        0.0,
        -3.0862664687972017,
        1.1721513422464978,
        0.0,
        -2.22474487139,
        -2.22474487139,
        -1.0,
        0.0,
        -2.22474487139,
        -2.22474487139,
        1.0,
        0.0,
        -3.0862664687972017,
        -1.1721513422464978,
        0.0,
        0.0,
        -1.1721513422464978,
        -3.0862664687972017,
        0.0,
        0.0,
        -2.22474487139,
        -1.0,
        -2.22474487139,
        0.0,
        -2.22474487139,
        1.0,
        -2.22474487139,
        0.0,
        -1.1721513422464978,
        0.0,
        -3.0862664687972017,
        0.0,
        -3.0862664687972017,
        0.0,
        -1.1721513422464978,
        0.0,
        -2.22474487139,
        -1.0,
        2.22474487139,
        0.0,
        -2.22474487139,
        1.0,
        2.22474487139,
        0.0,
        -3.0862664687972017,
        0.0,
        1.1721513422464978,
        0.0,
        -1.1721513422464978,
        0.0,
        3.0862664687972017,
        0.0,
        -1.0,
        2.22474487139,
        -2.22474487139,
        0.0,
        1.0,
        2.22474487139,
        -2.22474487139,
        0.0,
        0.0,
        1.1721513422464978,
        -3.0862664687972017,
        0.0,
        0.0,
        3.0862664687972017,
        -1.1721513422464978,
        0.0,
        -1.0,
        2.22474487139,
        2.22474487139,
        0.0,
        1.0,
        2.22474487139,
        2.22474487139,
        0.0,
        0.0,
        3.0862664687972017,
        1.1721513422464978,
        0.0,
        0.0,
        1.1721513422464978,
        3.0862664687972017,
        0.0,
        2.22474487139,
        -2.22474487139,
        -1.0,
        0.0,
        2.22474487139,
        -2.22474487139,
        1.0,
        0.0,
        1.1721513422464978,
        -3.0862664687972017,
        0.0,
        0.0,
        3.0862664687972017,
        -1.1721513422464978,
        0.0,
        0.0,
        2.22474487139,
        -1.0,
        -2.22474487139,
        0.0,
        2.22474487139,
        1.0,
        -2.22474487139,
        0.0,
        3.0862664687972017,
        0.0,
        -1.1721513422464978,
        0.0,
        1.1721513422464978,
        0.0,
        -3.0862664687972017,
        0.0,
        2.22474487139,
        -1.0,
        2.22474487139,
        0.0,
        2.22474487139,
        1.0,
        2.22474487139,
        0.0,
        1.1721513422464978,
        0.0,
        3.0862664687972017,
        0.0,
        3.0862664687972017,
        0.0,
        1.1721513422464978,
        0.0,
    ]

    for _gradient_i in range(len(_gradient3)):
        _gradient3[_gradient_i] = _gradient3[_gradient_i] / _NORMALIZER_3D

    _gradient_j = 0
    for _gradient_i in range(_N_GRADS_3D * 2):
        if _gradient_j == len(_gradient3):
            _gradient_j = 0
        _GRADIENTS_3D.append(_gradient3[_gradient_j])
        _gradient_j += 1

    _gradient4 = [
        -0.6740059517812944,
        -0.3239847771997537,
        -0.3239847771997537,
        0.5794684678643381,
        -0.7504883828755602,
        -0.4004672082940195,
        0.15296486218853164,
        0.5029860367700724,
        -0.7504883828755602,
        0.15296486218853164,
        -0.4004672082940195,
        0.5029860367700724,
        -0.8828161875373585,
        0.08164729285680945,
        0.08164729285680945,
        0.4553054119602712,
        -0.4553054119602712,
        -0.08164729285680945,
        -0.08164729285680945,
        0.8828161875373585,
        -0.5029860367700724,
        -0.15296486218853164,
        0.4004672082940195,
        0.7504883828755602,
        -0.5029860367700724,
        0.4004672082940195,
        -0.15296486218853164,
        0.7504883828755602,
        -0.5794684678643381,
        0.3239847771997537,
        0.3239847771997537,
        0.6740059517812944,
        -0.6740059517812944,
        -0.3239847771997537,
        0.5794684678643381,
        -0.3239847771997537,
        -0.7504883828755602,
        -0.4004672082940195,
        0.5029860367700724,
        0.15296486218853164,
        -0.7504883828755602,
        0.15296486218853164,
        0.5029860367700724,
        -0.4004672082940195,
        -0.8828161875373585,
        0.08164729285680945,
        0.4553054119602712,
        0.08164729285680945,
        -0.4553054119602712,
        -0.08164729285680945,
        0.8828161875373585,
        -0.08164729285680945,
        -0.5029860367700724,
        -0.15296486218853164,
        0.7504883828755602,
        0.4004672082940195,
        -0.5029860367700724,
        0.4004672082940195,
        0.7504883828755602,
        -0.15296486218853164,
        -0.5794684678643381,
        0.3239847771997537,
        0.6740059517812944,
        0.3239847771997537,
        -0.6740059517812944,
        0.5794684678643381,
        -0.3239847771997537,
        -0.3239847771997537,
        -0.7504883828755602,
        0.5029860367700724,
        -0.4004672082940195,
        0.15296486218853164,
        -0.7504883828755602,
        0.5029860367700724,
        0.15296486218853164,
        -0.4004672082940195,
        -0.8828161875373585,
        0.4553054119602712,
        0.08164729285680945,
        0.08164729285680945,
        -0.4553054119602712,
        0.8828161875373585,
        -0.08164729285680945,
        -0.08164729285680945,
        -0.5029860367700724,
        0.7504883828755602,
        -0.15296486218853164,
        0.4004672082940195,
        -0.5029860367700724,
        0.7504883828755602,
        0.4004672082940195,
        -0.15296486218853164,
        -0.5794684678643381,
        0.6740059517812944,
        0.3239847771997537,
        0.3239847771997537,
        0.5794684678643381,
        -0.6740059517812944,
        -0.3239847771997537,
        -0.3239847771997537,
        0.5029860367700724,
        -0.7504883828755602,
        -0.4004672082940195,
        0.15296486218853164,
        0.5029860367700724,
        -0.7504883828755602,
        0.15296486218853164,
        -0.4004672082940195,
        0.4553054119602712,
        -0.8828161875373585,
        0.08164729285680945,
        0.08164729285680945,
        0.8828161875373585,
        -0.4553054119602712,
        -0.08164729285680945,
        -0.08164729285680945,
        0.7504883828755602,
        -0.5029860367700724,
        -0.15296486218853164,
        0.4004672082940195,
        0.7504883828755602,
        -0.5029860367700724,
        0.4004672082940195,
        -0.15296486218853164,
        0.6740059517812944,
        -0.5794684678643381,
        0.3239847771997537,
        0.3239847771997537,
        -0.753341017856078,
        -0.37968289875261624,
        -0.37968289875261624,
        -0.37968289875261624,
        -0.7821684431180708,
        -0.4321472685365301,
        -0.4321472685365301,
        0.12128480194602098,
        -0.7821684431180708,
        -0.4321472685365301,
        0.12128480194602098,
        -0.4321472685365301,
        -0.7821684431180708,
        0.12128480194602098,
        -0.4321472685365301,
        -0.4321472685365301,
        -0.8586508742123365,
        -0.508629699630796,
        0.044802370851755174,
        0.044802370851755174,
        -0.8586508742123365,
        0.044802370851755174,
        -0.508629699630796,
        0.044802370851755174,
        -0.8586508742123365,
        0.044802370851755174,
        0.044802370851755174,
        -0.508629699630796,
        -0.9982828964265062,
        -0.03381941603233842,
        -0.03381941603233842,
        -0.03381941603233842,
        -0.37968289875261624,
        -0.753341017856078,
        -0.37968289875261624,
        -0.37968289875261624,
        -0.4321472685365301,
        -0.7821684431180708,
        -0.4321472685365301,
        0.12128480194602098,
        -0.4321472685365301,
        -0.7821684431180708,
        0.12128480194602098,
        -0.4321472685365301,
        0.12128480194602098,
        -0.7821684431180708,
        -0.4321472685365301,
        -0.4321472685365301,
        -0.508629699630796,
        -0.8586508742123365,
        0.044802370851755174,
        0.044802370851755174,
        0.044802370851755174,
        -0.8586508742123365,
        -0.508629699630796,
        0.044802370851755174,
        0.044802370851755174,
        -0.8586508742123365,
        0.044802370851755174,
        -0.508629699630796,
        -0.03381941603233842,
        -0.9982828964265062,
        -0.03381941603233842,
        -0.03381941603233842,
        -0.37968289875261624,
        -0.37968289875261624,
        -0.753341017856078,
        -0.37968289875261624,
        -0.4321472685365301,
        -0.4321472685365301,
        -0.7821684431180708,
        0.12128480194602098,
        -0.4321472685365301,
        0.12128480194602098,
        -0.7821684431180708,
        -0.4321472685365301,
        0.12128480194602098,
        -0.4321472685365301,
        -0.7821684431180708,
        -0.4321472685365301,
        -0.508629699630796,
        0.044802370851755174,
        -0.8586508742123365,
        0.044802370851755174,
        0.044802370851755174,
        -0.508629699630796,
        -0.8586508742123365,
        0.044802370851755174,
        0.044802370851755174,
        0.044802370851755174,
        -0.8586508742123365,
        -0.508629699630796,
        -0.03381941603233842,
        -0.03381941603233842,
        -0.9982828964265062,
        -0.03381941603233842,
        -0.37968289875261624,
        -0.37968289875261624,
        -0.37968289875261624,
        -0.753341017856078,
        -0.4321472685365301,
        -0.4321472685365301,
        0.12128480194602098,
        -0.7821684431180708,
        -0.4321472685365301,
        0.12128480194602098,
        -0.4321472685365301,
        -0.7821684431180708,
        0.12128480194602098,
        -0.4321472685365301,
        -0.4321472685365301,
        -0.7821684431180708,
        -0.508629699630796,
        0.044802370851755174,
        0.044802370851755174,
        -0.8586508742123365,
        0.044802370851755174,
        -0.508629699630796,
        0.044802370851755174,
        -0.8586508742123365,
        0.044802370851755174,
        0.044802370851755174,
        -0.508629699630796,
        -0.8586508742123365,
        -0.03381941603233842,
        -0.03381941603233842,
        -0.03381941603233842,
        -0.9982828964265062,
        -0.3239847771997537,
        -0.6740059517812944,
        -0.3239847771997537,
        0.5794684678643381,
        -0.4004672082940195,
        -0.7504883828755602,
        0.15296486218853164,
        0.5029860367700724,
        0.15296486218853164,
        -0.7504883828755602,
        -0.4004672082940195,
        0.5029860367700724,
        0.08164729285680945,
        -0.8828161875373585,
        0.08164729285680945,
        0.4553054119602712,
        -0.08164729285680945,
        -0.4553054119602712,
        -0.08164729285680945,
        0.8828161875373585,
        -0.15296486218853164,
        -0.5029860367700724,
        0.4004672082940195,
        0.7504883828755602,
        0.4004672082940195,
        -0.5029860367700724,
        -0.15296486218853164,
        0.7504883828755602,
        0.3239847771997537,
        -0.5794684678643381,
        0.3239847771997537,
        0.6740059517812944,
        -0.3239847771997537,
        -0.3239847771997537,
        -0.6740059517812944,
        0.5794684678643381,
        -0.4004672082940195,
        0.15296486218853164,
        -0.7504883828755602,
        0.5029860367700724,
        0.15296486218853164,
        -0.4004672082940195,
        -0.7504883828755602,
        0.5029860367700724,
        0.08164729285680945,
        0.08164729285680945,
        -0.8828161875373585,
        0.4553054119602712,
        -0.08164729285680945,
        -0.08164729285680945,
        -0.4553054119602712,
        0.8828161875373585,
        -0.15296486218853164,
        0.4004672082940195,
        -0.5029860367700724,
        0.7504883828755602,
        0.4004672082940195,
        -0.15296486218853164,
        -0.5029860367700724,
        0.7504883828755602,
        0.3239847771997537,
        0.3239847771997537,
        -0.5794684678643381,
        0.6740059517812944,
        -0.3239847771997537,
        -0.6740059517812944,
        0.5794684678643381,
        -0.3239847771997537,
        -0.4004672082940195,
        -0.7504883828755602,
        0.5029860367700724,
        0.15296486218853164,
        0.15296486218853164,
        -0.7504883828755602,
        0.5029860367700724,
        -0.4004672082940195,
        0.08164729285680945,
        -0.8828161875373585,
        0.4553054119602712,
        0.08164729285680945,
        -0.08164729285680945,
        -0.4553054119602712,
        0.8828161875373585,
        -0.08164729285680945,
        -0.15296486218853164,
        -0.5029860367700724,
        0.7504883828755602,
        0.4004672082940195,
        0.4004672082940195,
        -0.5029860367700724,
        0.7504883828755602,
        -0.15296486218853164,
        0.3239847771997537,
        -0.5794684678643381,
        0.6740059517812944,
        0.3239847771997537,
        -0.3239847771997537,
        -0.3239847771997537,
        0.5794684678643381,
        -0.6740059517812944,
        -0.4004672082940195,
        0.15296486218853164,
        0.5029860367700724,
        -0.7504883828755602,
        0.15296486218853164,
        -0.4004672082940195,
        0.5029860367700724,
        -0.7504883828755602,
        0.08164729285680945,
        0.08164729285680945,
        0.4553054119602712,
        -0.8828161875373585,
        -0.08164729285680945,
        -0.08164729285680945,
        0.8828161875373585,
        -0.4553054119602712,
        -0.15296486218853164,
        0.4004672082940195,
        0.7504883828755602,
        -0.5029860367700724,
        0.4004672082940195,
        -0.15296486218853164,
        0.7504883828755602,
        -0.5029860367700724,
        0.3239847771997537,
        0.3239847771997537,
        0.6740059517812944,
        -0.5794684678643381,
        -0.3239847771997537,
        0.5794684678643381,
        -0.6740059517812944,
        -0.3239847771997537,
        -0.4004672082940195,
        0.5029860367700724,
        -0.7504883828755602,
        0.15296486218853164,
        0.15296486218853164,
        0.5029860367700724,
        -0.7504883828755602,
        -0.4004672082940195,
        0.08164729285680945,
        0.4553054119602712,
        -0.8828161875373585,
        0.08164729285680945,
        -0.08164729285680945,
        0.8828161875373585,
        -0.4553054119602712,
        -0.08164729285680945,
        -0.15296486218853164,
        0.7504883828755602,
        -0.5029860367700724,
        0.4004672082940195,
        0.4004672082940195,
        0.7504883828755602,
        -0.5029860367700724,
        -0.15296486218853164,
        0.3239847771997537,
        0.6740059517812944,
        -0.5794684678643381,
        0.3239847771997537,
        -0.3239847771997537,
        0.5794684678643381,
        -0.3239847771997537,
        -0.6740059517812944,
        -0.4004672082940195,
        0.5029860367700724,
        0.15296486218853164,
        -0.7504883828755602,
        0.15296486218853164,
        0.5029860367700724,
        -0.4004672082940195,
        -0.7504883828755602,
        0.08164729285680945,
        0.4553054119602712,
        0.08164729285680945,
        -0.8828161875373585,
        -0.08164729285680945,
        0.8828161875373585,
        -0.08164729285680945,
        -0.4553054119602712,
        -0.15296486218853164,
        0.7504883828755602,
        0.4004672082940195,
        -0.5029860367700724,
        0.4004672082940195,
        0.7504883828755602,
        -0.15296486218853164,
        -0.5029860367700724,
        0.3239847771997537,
        0.6740059517812944,
        0.3239847771997537,
        -0.5794684678643381,
        0.5794684678643381,
        -0.3239847771997537,
        -0.6740059517812944,
        -0.3239847771997537,
        0.5029860367700724,
        -0.4004672082940195,
        -0.7504883828755602,
        0.15296486218853164,
        0.5029860367700724,
        0.15296486218853164,
        -0.7504883828755602,
        -0.4004672082940195,
        0.4553054119602712,
        0.08164729285680945,
        -0.8828161875373585,
        0.08164729285680945,
        0.8828161875373585,
        -0.08164729285680945,
        -0.4553054119602712,
        -0.08164729285680945,
        0.7504883828755602,
        -0.15296486218853164,
        -0.5029860367700724,
        0.4004672082940195,
        0.7504883828755602,
        0.4004672082940195,
        -0.5029860367700724,
        -0.15296486218853164,
        0.6740059517812944,
        0.3239847771997537,
        -0.5794684678643381,
        0.3239847771997537,
        0.5794684678643381,
        -0.3239847771997537,
        -0.3239847771997537,
        -0.6740059517812944,
        0.5029860367700724,
        -0.4004672082940195,
        0.15296486218853164,
        -0.7504883828755602,
        0.5029860367700724,
        0.15296486218853164,
        -0.4004672082940195,
        -0.7504883828755602,
        0.4553054119602712,
        0.08164729285680945,
        0.08164729285680945,
        -0.8828161875373585,
        0.8828161875373585,
        -0.08164729285680945,
        -0.08164729285680945,
        -0.4553054119602712,
        0.7504883828755602,
        -0.15296486218853164,
        0.4004672082940195,
        -0.5029860367700724,
        0.7504883828755602,
        0.4004672082940195,
        -0.15296486218853164,
        -0.5029860367700724,
        0.6740059517812944,
        0.3239847771997537,
        0.3239847771997537,
        -0.5794684678643381,
        0.03381941603233842,
        0.03381941603233842,
        0.03381941603233842,
        0.9982828964265062,
        -0.044802370851755174,
        -0.044802370851755174,
        0.508629699630796,
        0.8586508742123365,
        -0.044802370851755174,
        0.508629699630796,
        -0.044802370851755174,
        0.8586508742123365,
        -0.12128480194602098,
        0.4321472685365301,
        0.4321472685365301,
        0.7821684431180708,
        0.508629699630796,
        -0.044802370851755174,
        -0.044802370851755174,
        0.8586508742123365,
        0.4321472685365301,
        -0.12128480194602098,
        0.4321472685365301,
        0.7821684431180708,
        0.4321472685365301,
        0.4321472685365301,
        -0.12128480194602098,
        0.7821684431180708,
        0.37968289875261624,
        0.37968289875261624,
        0.37968289875261624,
        0.753341017856078,
        0.03381941603233842,
        0.03381941603233842,
        0.9982828964265062,
        0.03381941603233842,
        -0.044802370851755174,
        0.044802370851755174,
        0.8586508742123365,
        0.508629699630796,
        -0.044802370851755174,
        0.508629699630796,
        0.8586508742123365,
        -0.044802370851755174,
        -0.12128480194602098,
        0.4321472685365301,
        0.7821684431180708,
        0.4321472685365301,
        0.508629699630796,
        -0.044802370851755174,
        0.8586508742123365,
        -0.044802370851755174,
        0.4321472685365301,
        -0.12128480194602098,
        0.7821684431180708,
        0.4321472685365301,
        0.4321472685365301,
        0.4321472685365301,
        0.7821684431180708,
        -0.12128480194602098,
        0.37968289875261624,
        0.37968289875261624,
        0.753341017856078,
        0.37968289875261624,
        0.03381941603233842,
        0.9982828964265062,
        0.03381941603233842,
        0.03381941603233842,
        -0.044802370851755174,
        0.8586508742123365,
        -0.044802370851755174,
        0.508629699630796,
        -0.044802370851755174,
        0.8586508742123365,
        0.508629699630796,
        -0.044802370851755174,
        -0.12128480194602098,
        0.7821684431180708,
        0.4321472685365301,
        0.4321472685365301,
        0.508629699630796,
        0.8586508742123365,
        -0.044802370851755174,
        -0.044802370851755174,
        0.4321472685365301,
        0.7821684431180708,
        -0.12128480194602098,
        0.4321472685365301,
        0.4321472685365301,
        0.7821684431180708,
        0.4321472685365301,
        -0.12128480194602098,
        0.37968289875261624,
        0.753341017856078,
        0.37968289875261624,
        0.37968289875261624,
        0.9982828964265062,
        0.03381941603233842,
        0.03381941603233842,
        0.03381941603233842,
        0.8586508742123365,
        -0.044802370851755174,
        -0.044802370851755174,
        0.508629699630796,
        0.8586508742123365,
        -0.044802370851755174,
        0.508629699630796,
        -0.044802370851755174,
        0.7821684431180708,
        -0.12128480194602098,
        0.4321472685365301,
        0.4321472685365301,
        0.8586508742123365,
        0.508629699630796,
        -0.044802370851755174,
        -0.044802370851755174,
        0.7821684431180708,
        0.4321472685365301,
        -0.12128480194602098,
        0.4321472685365301,
        0.7821684431180708,
        0.4321472685365301,
        0.4321472685365301,
        -0.12128480194602098,
        0.753341017856078,
        0.37968289875261624,
        0.37968289875261624,
        0.37968289875261624,
    ]

    for _gradient_i in range(len(_gradient4)):
        _gradient4[_gradient_i] = _gradient4[_gradient_i] / _NORMALIZER_4D

    _gradient_j = 0
    for _gradient_i in range(_N_GRADS_4D * 2):
        if _gradient_j == len(_gradient4):
            _gradient_j = 0
        _GRADIENTS_4D.append(_gradient4[_gradient_j])
        _gradient_j += 1
