#pragma once
// Shared data formats. Keep identical to src/ecv_common/types.py.
#include <array>
#include <cstdint>
#include <optional>
#include <string>
#include <vector>

namespace ecv {

struct Detection {
  std::string cls;
  float score = 0.f;
  std::array<float, 4> xyxy{};
};

struct Track {
  int id = 0;
  std::string cls;
  std::array<float, 4> xyxy{};
  std::optional<std::array<double, 2>> ground_xy_m;
  std::optional<double> speed_kmh;
};

struct FrameRecord {
  std::int64_t frame = 0;
  std::int64_t t_ns = 0;
  std::vector<Detection> dets;
  std::vector<Track> tracks;
};

// One JSON Lines record (no trailing newline), same field order as the Python writer.
std::string to_json_line(const FrameRecord& r);

}  // namespace ecv
