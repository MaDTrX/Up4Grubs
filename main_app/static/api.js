const fetch = require('node-fetch')

// const key = 'AIzaSyDiH0QlCu3l2RAkwcOgav_N891BxYmuEf4'
// const api =  `https://maps.googleapis.com/maps/api/geocode/json?address=3020+Van+Buren+blvd,+riverside+ca+92503&key=${key}`

// async function latLong () {
//     let response = await fetch (api)
//     let data =  await response.json()
    
//     console.log(data.results[0].geometry.location.lat)
//     console.log(data.results[0].geometry.location.lng)
// }
// latLong()
// async function initMap() {
    
//    response = await fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=Harrison Square Apartments, 312 2nd Avenue West, Seattle, WA, USA&key=AIzaSyDiH0QlCu3l2RAkwcOgav_N891BxYmuEf4`)
//     let data = await response.json()
//     let result = data.results
//    console.log(result)
//    let lat, lng
//    for (element of result){
//        lat = element.geometry.location.lat
//        lng = element.geometry.location.lng
//     }
//     console.log(typeof lat, lng)
// }
// console.log(initMap())