#include "ecv/common/geometry.hpp"

#include <stdexcept>

namespace ecv {
namespace {

std::array<double, 2> apply(const std::array<double, 9>& m, double a, double b) {
  const double w = m[6] * a + m[7] * b + m[8];
  if (w == 0.0) throw std::domain_error("point at infinity");
  return {(m[0] * a + m[1] * b + m[2]) / w, (m[3] * a + m[4] * b + m[5]) / w};
}

std::array<double, 9> inverse(const std::array<double, 9>& m) {
  const double a = m[0], b = m[1], c = m[2], d = m[3], e = m[4], f = m[5], g = m[6], h = m[7],
               i = m[8];
  const double det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g);
  if (det == 0.0) throw std::domain_error("singular homography");
  const double k = 1.0 / det;
  return {(e * i - f * h) * k, (c * h - b * i) * k, (b * f - c * e) * k,
          (f * g - d * i) * k, (a * i - c * g) * k, (c * d - a * f) * k,
          (d * h - e * g) * k, (b * g - a * h) * k, (a * e - b * d) * k};
}

}  // namespace

std::array<double, 2> Homography::pixel_to_ground(double u, double v) const {
  return apply(h, u, v);
}

std::array<double, 2> Homography::ground_to_pixel(double x, double y) const {
  return apply(inverse(h), x, y);
}

}  // namespace ecv
