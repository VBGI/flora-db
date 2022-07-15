let header = document.querySelector('h1').childNodes[0].innerHTML
let centers = coordinates
let body = ''

console.log(coordinates)

function init(){

    // Создаем карту
    var map = new ymaps.Map("map", {
        center: [55, 37], // координаты центра карты, при загрузке
        zoom: 10  // коэффициент масштабирования
    });

    //Добавляем в геокодер список адресов

    var objects = ymaps.geoQuery(ymaps.geocode(centers[0], {results: 1}))
    for(var i = 1; i < centers.length; i++){
        objects = objects.add(ymaps.geocode(centers[i], {results: 1}))
    }
    // objects.addToMap(map);


    // Создаем коллекцию геообъектов, в котором будут находиться эти адреса
    var geoObjectsCollection = new ymaps.GeoObjectCollection();

    // После того, как поиск вернул результат, вызывается callback-функция
    objects.then(function () {

        // добавляем координаты адресов в коллекцию geoObjectsCollection
        objects.each(function (object) {

            var coordinates = object.geometry.getCoordinates();


            body = object.properties._data.description

            geoObjectsCollection.add( new ymaps.Placemark(coordinates, {
                balloonContentHeader: header,
                balloonContentBody: body,
            }, {
                iconLayout: 'default#image',
                iconImageHref: 'https://cdn-icons-png.flaticon.com/512/684/684908.png',
                iconImageSize: [30,30],
                iconImageOffset: [-15, -30]
            }));

        });

        // Добавляем коллекцию геообъектов на карту
        map.geoObjects.add(geoObjectsCollection);

        // Спозиционируем карту так, чтобы на ней были видны все объекты.
        map.setBounds(geoObjectsCollection.getBounds());

        map.controls.remove('trafficControl'); // удаляем контроль трафика
        map.controls.remove('zoomControl'); // удаляем контрол зуммирования



    });


}


ymaps.ready(init);