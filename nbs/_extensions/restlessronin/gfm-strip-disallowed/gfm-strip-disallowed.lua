-- reference for disallowed tags
-- https://github.github.com/gfm/#disallowed-raw-html-extension-
disallowed_raw = {"title","textarea","style","xmp","iframe","noembed","noframes","script","plaintext","style scoped"}
disallowed_open = pandoc.List(disallowed_raw):map(function(tag) return "<" .. tag .. ">" end)
disallowed_close = pandoc.List(disallowed_raw):map(function(tag) return "</" .. tag .. ">" end)

function starts_with(text, tag)
  return text:find(tag, 1, true) == 1
end

function is_disallowed_block(raw_text)
  -- Check if the text starts with any disallowed opening tag
  if disallowed_open:find_if(function(tag) return starts_with(raw_text, tag) end, 1) then
    return true
  end
  -- Check if the text contains any disallowed closing tag
  if disallowed_close:find_if(function(tag) return raw_text:find(tag, 1, true) end, 1) then
    return true
  end
  return false
end

function ltrim(str)
  return str:gsub("^%s+", "")
end

function RawBlock(rawEl)
  if rawEl.format == "html" and is_disallowed_block(ltrim(rawEl.text)) then
    return pandoc.List({})
  else
    return nil
  end
end
