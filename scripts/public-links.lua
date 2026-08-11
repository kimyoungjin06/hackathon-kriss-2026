local routes = {
  ["PROGRAM.md"] = "../program/",
  ["API_GUIDE.md"] = "../api/",
  ["PARTICIPANT_GUIDE.md"] = "../guide/",
  ["EXAMPLES.md"] = "../examples/",
  ["SOURCES.md"] = "../sources/",
  ["RIGHTS_AND_ATTRIBUTION.md"] = "../rights/",
  ["README.md"] = "../",
  ["README.md#데이터-안전-원칙"] = "../guide/#데이터-규칙",
  ["demo/index.html"] = "../demo/"
}

local title_removed = false

function Header(element)
  if not title_removed and element.level == 1 then
    title_removed = true
    return {}
  end
end

function Link(element)
  local replacement = routes[element.target]
  if replacement then
    element.target = replacement
  end
  return element
end
