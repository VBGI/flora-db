let header = document.querySelector('h1').childNodes[0].innerHTML
let center = [43.024431, 131.894045];
let body = ''


function init(){

    //взятие названия местности по координатм
    res =  ymaps.geocode(center, {
        results: 1
    }).then(function (res) {
            // Выбираем первый результат геокодирования.
            firstGeoObject = res.geoObjects.get(0);

            body = firstGeoObject.properties.get('description');


            let map = new ymaps.Map('map', {
                center: center,
                zoom: 16
            })


            let placemark = new ymaps.Placemark(center, {
                balloonContentHeader: header,
                balloonContentBody: body,
            }, {
                iconLayout: 'default#image',
                iconImageHref: 'https://cdn-icons-png.flaticon.com/512/684/684908.png',
                iconImageSize: [30,30],
                iconImageOffset: [-25, -30]
            })

            console.log()

            map.controls.remove('geolocationControl'); // удаляем геолокацию
            map.controls.remove('trafficControl'); // удаляем контроль трафика
            map.controls.remove('zoomControl'); // удаляем контрол зуммирования

            map.geoObjects.add(placemark)


            placemark.balloon.open();

    });
}


ymaps.ready(init);