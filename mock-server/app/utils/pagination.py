def paginate(data, page=1, limit=10):
  page = max(page, 1)
  limit = max(limit, 1)

  start = (page - 1) * limit
  end = start + limit
  
  items = data[start:end]

  total = len(data)

  return {
    "data": items,
    "total": total,
    "page": page,
    "limit": limit
  }
