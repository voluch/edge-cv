#pragma once
#include <array>

namespace ecv {

// 3x3 homography mapping image pixels to ground-plane metres (row-major).
struct Homography {
  std::array<double, 9> h{1, 0, 0, 0, 1, 0, 0, 0, 1};

  std::array<double, 2> pixel_to_ground(double u, double v) const;
  std::array<double, 2> ground_to_pixel(double x, double y) const;
};

}  // namespace ecv
