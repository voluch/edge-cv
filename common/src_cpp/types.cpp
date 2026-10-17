#include "ecv/common/types.hpp"

#include <cstdio>
#include <sstream>

namespace ecv {
namespace {

std::string num(double v, int digits = 10) {
  char buf[64];
  std::snprintf(buf, sizeof buf, "%.*g", digits, v);
  return buf;
}

// float values are printed with 7 significant digits so 0.91f prints as 0.91
std::string num(float v) { return num(static_cast<double>(v), 7); }

template <std::size_t N, typename T>
std::string arr(const std::array<T, N>& a) {
  std::string s = "[";
  for (std::size_t i = 0; i < N; ++i) s += (i ? "," : "") + num(a[i]);
  return s + "]";
}

}  // namespace

std::string to_json_line(const FrameRecord& r) {
  std::ostringstream o;
  o << "{\"frame\":" << r.frame << ",\"t_ns\":" << r.t_ns << ",\"dets\":[";
  for (std::size_t i = 0; i < r.dets.size(); ++i) {
    const auto& d = r.dets[i];
    o << (i ? "," : "") << "{\"cls\":\"" << d.cls << "\",\"score\":" << num(d.score)
      << ",\"xyxy\":" << arr(d.xyxy) << "}";
  }
  o << "],\"tracks\":[";
  for (std::size_t i = 0; i < r.tracks.size(); ++i) {
    const auto& t = r.tracks[i];
    o << (i ? "," : "") << "{\"id\":" << t.id << ",\"cls\":\"" << t.cls
      << "\",\"xyxy\":" << arr(t.xyxy);
    if (t.ground_xy_m) o << ",\"ground_xy_m\":" << arr(*t.ground_xy_m);
    if (t.speed_kmh) o << ",\"speed_kmh\":" << num(*t.speed_kmh);
    o << "}";
  }
  o << "]}";
  return o.str();
}

}  // namespace ecv
