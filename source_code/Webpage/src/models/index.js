
import Vue from 'vue'

function getPromise (url) {
  return Vue.http.get(url).then(res => {
    return Promise.resolve(res.body)
  }, () => {
    return Promise.reject(new Error('未知错误'))
  })
}

function postPromise (url, form) {
  return Vue.http.post(url, form, { emulateJSON: true }).then(res => {
    return Promise.resolve(res.body)
  }, () => {
    return Promise.reject(new Error('未知错误'))
  })
}

function putPromise (url, form) {
  return Vue.http.put(url, form, { emulateJSON: true }).then(res => {
    return Promise.resolve(res.body)
  }, () => {
    return Promise.reject(new Error('未知错误'))
  })
}

const User = {
  login (form) {
    return postPromise(`/api/login`, form)
  },
  logout () {
    return putPromise(`/api/logout`, {})
  },
  signup (form) {
    return postPromise(`/api/signup`, form)
  },
  fetchInfo () {
    return getPromise(`/api/user`)
  },
  updateInfo (form) {
    return putPromise(`/api/user`, form)
  },
  lockSeat (id, form) {
    return putPromise(`/api/user/screen/${id}`, form)
  },
  buySeat (id, form) {
    return putPromise(`/api/user/screen/${id}`, form)
  },
  getOrders () {
    return getPromise('/api/user/order')
  }
}

const Movie = {
  fetchDtl (id) {
    return getPromise(`/api/movie/${id}`)
  },
  fetchNews (n) {
    return getPromise(`/api/movie/showing/${n}`)
  },
  fetchMonth () {
    return getPromise(`/api/movie/date/month/201706`)
  },
  queryMovie (type, area, year, page, step) {
    return getPromise(`/api/movie/query?type=${type}&area=${area}&year=${year}&page=${page}&step=${step}`)
  },
  countMovie (type, area, year) {
    return getPromise(`/api/movie/query/count?type=${type}&area=${area}&year=${year}`)
  },
  search (keyword) {
    return getPromise(`/api/search?query=${keyword}`)
  }
}

const Cinema = {
  fetchCinemaByArea (area, num = 50) {
    return getPromise(`/api/cinema?number=${num}&address=${area}`)
  },
  fetchSeat (cid, mid, date, time) {
    return getPromise(`/api/screen?cinemaid=${cid}&movieid=${mid}&date=${date}&time=${time}`)
  }
}

const Screen = {
  getScreenById (id) {
    return getPromise(`/api/screen/${id}`)
  }
}

export { User, Movie, Cinema, Screen }
