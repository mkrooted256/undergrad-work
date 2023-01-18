# Lab Adv2. mongodb mapreduce
Mykhailo Koreshkov. FI-91

## -1. Collections
1. `products`
```
docker exec -it mongo-alone mongoexport -d adv2 -c products
2023-01-18T10:26:55.689+0000    connected to: mongodb://localhost/
{"_id":{"$oid":"63c7c8582b679c55e4039ee8"},"cat":"phone","model":"IPhone1","brand":"Apple","price":100}
{"_id":{"$oid":"63c7c85f2b679c55e4039ee9"},"cat":"phone","model":"IPhone2","brand":"Apple","price":150}
{"_id":{"$oid":"63c7c8702b679c55e4039eea"},"cat":"phone","model":"Xiaomi Mi125","brand":"Xiaomi","price":12}
{"_id":{"$oid":"63c7c8852b679c55e4039eeb"},"cat":"TV","model":"Samsung Q1","brand":"Samsung","price":200}
{"_id":{"$oid":"63c7c8932b679c55e4039eec"},"cat":"TV","model":"Samsung HD1","brand":"Samsung","price":150}
{"_id":{"$oid":"63c7c8a92b679c55e4039eed"},"cat":"TV","model":"Noname ELT1","brand":"Noname","price":50}
{"_id":{"$oid":"63c7c8c32b679c55e4039eee"},"cat":"Laptop","model":"Acer Aspire 5","brand":"Acer","price":105}
{"_id":{"$oid":"63c7c8cf2b679c55e4039eef"},"cat":"Laptop","model":"Acer Swift 7","brand":"Acer","price":215}
{"_id":{"$oid":"63c7c8e32b679c55e4039ef0"},"cat":"Laptop","model":"Lenovo Thinkpad T14s","brand":"Lenovo","price":250}
{"_id":{"$oid":"63c7c8f42b679c55e4039ef1"},"cat":"Laptop","model":"IBM Original Thinkpad","brand":"IBM","price":500}
{"_id":{"$oid":"63c7c9062b679c55e4039ef2"},"cat":"Laptop","model":"Macbook Air 2022","brand":"Apple","price":400}
{"_id":{"$oid":"63c7c90a2b679c55e4039ef3"},"cat":"Laptop","model":"Macbook Air 2023","brand":"Apple","price":500}
2023-01-18T10:26:55.692+0000    exported 12 records
```

2. `orders`
```
docker exec -it mongo-alone mongoexport -d adv2 -c orders
2023-01-18T10:31:51.163+0000    connected to: mongodb://localhost/
{"_id":{"$oid":"63c7ca802b679c55e4039ef7"},"order_no":1,"date":{"$date":"2022-12-01T00:00:00Z"},"customer":{"name":"John","city":"Kyiv"},"items":[{"$oid":"63c7c8582b679c55e4039ee8"},{"$oid":"63c7c8932b679c55e4039eec"}]}
{"_id":{"$oid":"63c7ca802b679c55e4039ef8"},"order_no":2,"date":{"$date":"2022-12-02T00:00:00Z"},"customer":{"name":"Jane","city":"Kharkiv"},"items":[{"$oid":"63c7c90a2b679c55e4039ef3"},{"$oid":"63c7c8c32b679c55e4039eee"}]}
{"_id":{"$oid":"63c7ca802b679c55e4039ef9"},"order_no":3,"date":{"$date":"2022-12-02T00:00:00Z"},"customer":{"name":"Thomas","city":"Lviv"},"items":[{"$oid":"63c7c8f42b679c55e4039ef1"},{"$oid":"63c7c8f42b679c55e4039ef1"},{"$oid":"63c7c8702b679c55e4039eea"}]}
{"_id":{"$oid":"63c7ca802b679c55e4039efa"},"order_no":4,"date":{"$date":"2022-12-04T00:00:00Z"},"customer":{"name":"Thomas","city":"Lviv"},"items":[{"$oid":"63c7c8852b679c55e4039eeb"}]}
2023-01-18T10:31:51.167+0000    exported 4 records
```

## 0. Theory

Map та Reduce це операції, типові для функціональної парадигми програмування. 
Характерна відмінність від процедурного чи ОО програмування в тому, що ці операції є "функціями вищого порядку": вони приймають користувацьку функцію у якості свого аргумента.

На мою думку, найкраще дію цих функцій пояснюють нотація типів Haskell
```Haskell
map :: (a->b) -> [a] -> [b]
-- map( Map function, Input data ) -> Processed data
```
Map діє на кожен елемент вхідної колекції заданою фукнцією та утворює вихідну колекцію з результатів обчислень.

```Haskell
reduce :: (b->a->b) -> b -> [a] -> b
-- reduce( Operation to update an accumulator , Initial value of an accumulator , Input data ) -> Accumulated result 
```
Reduce це в деякому сенсі узагальнення суми колекції. 
Reduce ініціалізує змінну-акумулятор заданим значенням, а далі обчислює нове значення акумулятора для кожного елементу колекції.
Псевдокод:
```
In: op, init_acc, data
Out: acc
Alg:
1. acc <- init_acc
2. for d in data:
3.   acc <- op(acc, d)
4. return acc
```

Врешті-решт, mapReduce це послідовне застосування Map та Reduce.
З доків монго:
```
var mapFunction = function() { ... emit(key, value); };
var reduceFunction = function(key, values) { ... return result; };
var finalizeFunction = function(key, reducedValue) { ... return modifiedResult; };
db.runCommand(
               {
                 mapReduce: <input-collection>,
                 map: mapFunction,
                 reduce: reduceFunction,
                 finalize: finalizeFunction,
                 out: { merge: <output-collection> },
                 query: <query>
               }
             )
```

Відмінність від теоретичних map та reduce в тому, що тут для кожного елементу вхідної колекції map може повернути більше одного значення, або не повернути ніякого.
Також reduce тут має набагато більш строгі вимоги: reduce функція має бути асоціативною, комутативною, ідемпотентною.

Краса в тому, що із цими вимогами операцію map-reduce можна паралелізувати та обчислювати розподілено: як за даними, так і за обчисленнями.

## From MapReduce to Aggregation pipelines

```
DeprecationWarning: Collection.mapReduce() is deprecated. Use an aggregation instead.
See https://docs.mongodb.com/manual/core/map-reduce for details.
```
<!-- 
- `mapFunction` is now `project -> emits` combined with `unwind`
- `reduceFunction` is now `group` with ton of parameters -->

Тому буду використовувати aggregation pipelines.

## 1. Підрахувати скільки одиниць товару є у кожного виробника ("brand")

```javascript
test> use adv2
adv2> db.products.aggregate([ { $group: { _id: "$brand", value: { $sum: 1 } } }])
[
  { _id: 'Xiaomi', value: 1 },
  { _id: 'Acer', value: 2 },
  { _id: 'IBM', value: 1 },
  { _id: 'Samsung', value: 2 },
  { _id: 'Noname', value: 1 },
  { _id: 'Apple', value: 4 },
  { _id: 'Lenovo', value: 1 }
]
```

- Ключем групування буде поле brand
- Значення групи це сума ($sum) одиниць. по одиниці за кожну модель.

## 2. Підрахувати загальну вартість товарів у кожного виробника

```
adv2> db.products.aggregate([ { $group: { _id: "$brand", value: { $sum: "$price" } } }])
[
  { _id: 'Xiaomi', value: 12 },
  { _id: 'Acer', value: 320 },
  { _id: 'IBM', value: 500 },
  { _id: 'Samsung', value: 350 },
  { _id: 'Noname', value: 50 },
  { _id: 'Apple', value: 1150 },
  { _id: 'Lenovo', value: 250 }
]
```

## 3. Підрахуйте сумарну вартість замовлень зроблену кожним замовником

Спочатку я обчислю вартість кожного замовлення та збережу в бд:
```
adv2> db.orders.aggregate([ 
    {$lookup: {from: 'products', localField: 'items', foreignField: '_id', as: 'products'}}, 
    {$unwind: '$products'}, 
    {$group: { _id: '$_id', subtotal: {$sum: '$products.price'}}}, 
])
[
  { _id: ObjectId("63c7ca802b679c55e4039ef8"), subtotal: 605 },
  { _id: ObjectId("63c7ca802b679c55e4039ef7"), subtotal: 250 },
  { _id: ObjectId("63c7ca802b679c55e4039ef9"), subtotal: 512 },
  { _id: ObjectId("63c7ca802b679c55e4039efa"), subtotal: 200 }
]

adv2> db.orders.aggregate([ 
    {$lookup: {from: 'products', localField: 'items', foreignField: '_id', as: 'products'}}, 
    {$unwind: '$products'}, 
    {$group: { _id: '$_id', subtotal: {$sum: '$products.price'}}}, 
    {$merge: {into: 'orders'}}
])

docker exec -it mongo-alone mongoexport -d adv2 -c orders
2023-01-18T11:55:53.376+0000    connected to: mongodb://localhost/
{"_id":{"$oid":"63c7ca802b679c55e4039ef7"},"order_no":1,"date":{"$date":"2022-12-01T00:00:00Z"},"customer":{"name":"John","city":"Kyiv"},"items":[{"$oid":"63c7c8582b679c55e4039ee8"},{"$oid":"63c7c8932b679c55e4039eec"}],"subtotal":250}
{"_id":{"$oid":"63c7ca802b679c55e4039ef8"},"order_no":2,"date":{"$date":"2022-12-02T00:00:00Z"},"customer":{"name":"Jane","city":"Kharkiv"},"items":[{"$oid":"63c7c90a2b679c55e4039ef3"},{"$oid":"63c7c8c32b679c55e4039eee"}],"subtotal":605}
{"_id":{"$oid":"63c7ca802b679c55e4039ef9"},"order_no":3,"date":{"$date":"2022-12-02T00:00:00Z"},"customer":{"name":"Thomas","city":"Lviv"},"items":[{"$oid":"63c7c8f42b679c55e4039ef1"},{"$oid":"63c7c8f42b679c55e4039ef1"},{"$oid":"63c7c8702b679c55e4039eea"}],"subtotal":512}
{"_id":{"$oid":"63c7ca802b679c55e4039efa"},"order_no":4,"date":{"$date":"2022-12-04T00:00:00Z"},"customer":{"name":"Thomas","city":"Lviv"},"items":[{"$oid":"63c7c8852b679c55e4039eeb"}],"subtotal":200}
2023-01-18T11:55:53.380+0000    exported 4 records
```

Далі сумарні витрати кожного замовника:

```
adv2> db.orders.aggregate([ 
    { $group: { _id: '$customer', subtotal: { $sum: '$subtotal' } } }
])
[
  { _id: { name: 'Jane', city: 'Kharkiv' }, subtotal: 605 },
  { _id: { name: 'John', city: 'Kyiv' }, subtotal: 250 },
  { _id: { name: 'Thomas', city: 'Lviv' }, subtotal: 712 }
]
```

## 4. Підрахуйте сумарну вартість замовлень зроблену кожним замовником за певний період часу (використовуйте query condition)

```
adv2> db.orders.aggregate([ 
    {$match: {date: {$lt: new ISODate("2022-12-03")}}}, 
    { $group: { _id: '$customer', subtotal: { $sum: '$subtotal' } } }
])
[
  { _id: { name: 'Jane', city: 'Kharkiv' }, subtotal: 605 },
  { _id: { name: 'John', city: 'Kyiv' }, subtotal: 250 },
  { _id: { name: 'Thomas', city: 'Lviv' }, subtotal: 512 }
]
```

## 5. Підрахуйте середню вартість замовлення

```
adv2> db.orders.aggregate([ 
    { $group: { _id: null, avgsubtotal: { $avg: '$subtotal' } } }
])
[ { _id: null, avgsubtotal: 391.75 } ]
```

## 6. Підрахуйте середню вартість замовлення кожного покупця
```
adv2> db.orders.aggregate([ 
    { $group: { _id: '$customer', avgsubtotal: { $avg: '$subtotal' } } }
])
[
  { _id: { name: 'Jane', city: 'Kharkiv' }, avgsubtotal: 605 },
  { _id: { name: 'Thomas', city: 'Lviv' }, avgsubtotal: 356 },
  { _id: { name: 'John', city: 'Kyiv' }, avgsubtotal: 250 }
]
```

## 7. Підрахуйте в скількох замовленнях зустрічався кожен товар (скільки разів він був куплений)
```
db.orders.aggregate([ 
    { $unwind: '$items' }, 
    { $group: { _id: '$items', item_count: { $sum: 1 } } }, 
    { $lookup: {from: 'products', localField: '_id', foreignField: '_id', as: 'product'}}, 
    { $project: {item_count: 1, _id: {$arrayElemAt: ['$product.model', 0]} }},
])
[
  { item_count: 1, _id: 'Xiaomi Mi125' },
  { item_count: 1, _id: 'Acer Aspire 5' },
  { item_count: 2, _id: 'Samsung Q1' },
  { item_count: 1, _id: 'Samsung HD1' },
  { item_count: 2, _id: 'IBM Original Thinkpad' },
  { item_count: 1, _id: 'Macbook Air 2023' },
  { item_count: 1, _id: 'IPhone1' }
]
```

## 8. Для кожного товару отримаєте список всіх замовників які купили його

Так вийшло, що в мене всі купували різне. Тому попередньо додаю нове замовлення.
```
adv2> db.orders.insertOne({"order_no":4,"date":{"$date":"2022-12-04T00:00:00Z"},"customer":{"name":"NotThomas","city":"NotLviv"},"items":[ObjectId("63c7c8852b679c55e4039eeb")],"subtotal":200})
{
  acknowledged: true,
  insertedId: ObjectId("63c7ea732857a38d4fb1ac4a")
}

adv2> db.orders.aggregate([ 
    { $unwind: '$items' }, 
    { $group: { _id: '$items', customers: { $addToSet: '$customer' } } }
])
[
  {
    _id: ObjectId("63c7c8702b679c55e4039eea"),
    customers: [ { name: 'Thomas', city: 'Lviv' } ]
  },
  {
    _id: ObjectId("63c7c8c32b679c55e4039eee"),
    customers: [ { name: 'Jane', city: 'Kharkiv' } ]
  },
  {
    _id: ObjectId("63c7c8852b679c55e4039eeb"),
    customers: [
      { name: 'Thomas', city: 'Lviv' },
      { name: 'NotThomas', city: 'NotLviv' }
    ]
  },
  {
    _id: ObjectId("63c7c8932b679c55e4039eec"),
    customers: [ { name: 'John', city: 'Kyiv' } ]
  },
  {
    _id: ObjectId("63c7c8f42b679c55e4039ef1"),
    customers: [ { name: 'Thomas', city: 'Lviv' } ]
  },
  {
    _id: ObjectId("63c7c90a2b679c55e4039ef3"),
    customers: [ { name: 'Jane', city: 'Kharkiv' } ]
  },
  {
    _id: ObjectId("63c7c8582b679c55e4039ee8"),
    customers: [ { name: 'John', city: 'Kyiv' } ]
  }
]
```

## 9. Отримайте товар та список замовників, які купували його більше одного (двох) разу(ів)

План такий:
1. Unwind продукти замовлення
2. Згрупувати за замовником та продуктом, обчислити кількість зустрічей кожної комбінації цих значень
3. Згрупувати за товаром, створити масив з тих замовників, які мають кількість більше 1

1.
```
adv2> db.orders.aggregate([ 
    { $unwind: '$items' }, 
    { $group: { _id: {customer:'$customer', item: '$items'}, item_count: {$sum: 1} } } 
])
[
  {
    _id: {
      customer: { name: 'Thomas', city: 'Lviv' },
      item: ObjectId("63c7c8852b679c55e4039eeb")
    },
    item_count: 1
  },
  {
    _id: {
      customer: { name: 'Thomas', city: 'Lviv' },
      item: ObjectId("63c7c8702b679c55e4039eea")
    },
    item_count: 1
  },
  {
    _id: {
      customer: { name: 'John', city: 'Kyiv' },
      item: ObjectId("63c7c8582b679c55e4039ee8")
    },
    item_count: 1
  },
  {
    _id: {
      customer: { name: 'NotThomas', city: 'NotLviv' },
      item: ObjectId("63c7c8852b679c55e4039eeb")
    },
    item_count: 1
  },
  {
    _id: {
      customer: { name: 'Thomas', city: 'Lviv' },
      item: ObjectId("63c7c8f42b679c55e4039ef1")
    },
    item_count: 2
  },
  {
    _id: {
      customer: { name: 'John', city: 'Kyiv' },
      item: ObjectId("63c7c8932b679c55e4039eec")
    },
    item_count: 1
  },
  {
    _id: {
      customer: { name: 'Jane', city: 'Kharkiv' },
      item: ObjectId("63c7c8c32b679c55e4039eee")
    },
    item_count: 1
  },
  {
    _id: {
      customer: { name: 'Jane', city: 'Kharkiv' },
      item: ObjectId("63c7c90a2b679c55e4039ef3")
    },
    item_count: 1
  }
]
```

2. (той самий запит, але додано ще 2 aggregation steps )
```
adv2> db.orders.aggregate([ 
    { $unwind: '$items' }, 
    { $group: { _id: {customer:'$customer', item: '$items'}, item_count: {$sum: 1} } }, 
    { $match: {'item_count': {$gt: 1}} }, 
    { $group: {_id: '$_id.item', customers: {$addToSet: '$_id.customer'}} } 
])
[
  {
    _id: ObjectId("63c7c8f42b679c55e4039ef1"),
    customers: [ { name: 'Thomas', city: 'Lviv' } ]
  }
]
```

## 10. Отримайте топ N товарів за популярністю (тобто топ товарів, які куплялись найчастіше) (функцію sort не застосовувати)
Беремо код з пункту 7 та додаємо topN в кінці

```
adv2> db.orders.aggregate([ 
    { $unwind: '$items' }, 
    { $group: { _id: '$items', item_count: { $sum: 1 } } }, 
    { $lookup: {from: 'products', localField: '_id', foreignField: '_id', as: 'product'}}, 
    { $project: {item_count: 1, _id: {$arrayElemAt: ['$product.model', 0]} }},

    { $group: { _id: null, top_items: 
        { $topN: { n: 5, output: ['$_id', '$item_count'], sortBy: {'item_count': -1} } }
    }}
])
[
  {
    _id: null,
    top_items: [
      [ 'Samsung Q1', 2 ],
      [ 'IBM Original Thinkpad', 2 ],
      [ 'IPhone1', 1 ],
      [ 'Acer Aspire 5', 1 ],
      [ 'Xiaomi Mi125', 1 ]
    ]
  }
]
```

## 11. Для завдання 4) реалізуйте інкрементальний Map / Reduce використовуючи out і action
Ось мій 4:
```
adv2> db.orders.aggregate([ 
    { $match: { date: { $lt: new ISODate("2022-12-06") } } }, 
    { $group: { _id: '$customer', subtotal: { $sum: '$subtotal' } } }
])
[
  { _id: { name: 'Jane', city: 'Kharkiv' }, subtotal: 605 },
  { _id: { name: 'Thomas', city: 'Lviv' }, subtotal: 712 },
  { _id: { name: 'John', city: 'Kyiv' }, subtotal: 250 },
  { _id: { name: 'NotThomas', city: 'NotLviv' }, subtotal: 200 }
]
```

Всі замовлення:
```
adv2> db.orders.find({}, {'customer.name':1, date: 1, _id:0})
[
  { date: ISODate("2022-12-01T00:00:00.000Z"), customer: { name: 'John' } },
  { date: ISODate("2022-12-02T00:00:00.000Z"), customer: { name: 'Jane' } },
  { date: ISODate("2022-12-02T00:00:00.000Z"), customer: { name: 'Thomas' } },
  { date: ISODate("2022-12-04T00:00:00.000Z"), customer: { name: 'Thomas' } },
  { date: ISODate("2022-12-04T00:00:00.000Z"), customer: { name: 'NotThomas' } }
]
```

Інкрементальна версія: додаємо merge.

За перший день
```
db.orders.aggregate([ 
    { $match: { date: { $gte: new ISODate("2022-12-01"), $lte: new ISODate("2022-12-01") } } }, 
    { $group: { _id: '$customer', subtotal: { $sum: '$subtotal' } } },
    { $merge: {
        into: 'task11res', 
        whenMatched: [{ $addFields: { subtotal: { $add: ['$subtotal', '$$new.subtotal'] }}}],
        whenNotMatched: 'insert'
    }}
])

adv2> db.task11res.find()
[ { _id: { name: 'John', city: 'Kyiv' }, subtotal: 250 } ]
```

За другий день
```
db.orders.aggregate([ 
    { $match: { date: { $gte: new ISODate("2022-12-02"), $lte: new ISODate("2022-12-02") } } }, 
    { $group: { _id: '$customer', subtotal: { $sum: '$subtotal' } } },
    { $merge: {
        into: 'task11res', 
        whenMatched: [{ $addFields: { subtotal: { $add: ['$subtotal', '$$new.subtotal'] }}}],
        whenNotMatched: 'insert'
    }}
])

adv2> db.task11res.find()
[
  { _id: { name: 'John', city: 'Kyiv' }, subtotal: 250 },
  { _id: { name: 'Jane', city: 'Kharkiv' }, subtotal: 605 },
  { _id: { name: 'Thomas', city: 'Lviv' }, subtotal: 512 }
]
```

За третій та четвертий дні
```
db.orders.aggregate([ 
    { $match: { date: { $gte: new ISODate("2022-12-03"), $lte: new ISODate("2022-12-04") } } }, 
    { $group: { _id: '$customer', subtotal: { $sum: '$subtotal' } } },
    { $merge: {
        into: 'task11res', 
        whenMatched: [{ $addFields: { subtotal: { $add: ['$subtotal', '$$new.subtotal'] }}}],
        whenNotMatched: 'insert'
    }}
])

adv2> db.task11res.find()
[
  { _id: { name: 'John', city: 'Kyiv' }, subtotal: 250 },
  { _id: { name: 'Jane', city: 'Kharkiv' }, subtotal: 605 },
  { _id: { name: 'Thomas', city: 'Lviv' }, subtotal: 712 },
  { _id: { name: 'NotThomas', city: 'NotLviv' }, subtotal: 200 }
]
```

## 12. Для кожного користувача, визначить на яку суму їм було зроблено замовлень за кожен місяць цього року та за аналогічний місяць минулого року та динаміку збільшення/зменшення замовлень.

Буду робити по парам днів, бо даних мало щоб обчислювати цілі місяці.

Вираз для daypair просто ставить у відповідність дням 1,2 пару 1 та дням 3,4 пару 2.

```javascript
db.orders.aggregate([
  { $group: { 
    _id: {
      customer: '$customer', 
      daypair: {$ceil: {$divide: [{$dayOfMonth: '$date'}, 2] }},
    }, 
    subtotal: { $sum: '$subtotal' } 
  }}
])

[
  {
    _id: { customer: { name: 'Thomas', city: 'Lviv' }, daypair: 1 },
    subtotal: 512
  },
  {
    _id: { customer: { name: 'NotThomas', city: 'NotLviv' }, daypair: 2 },
    subtotal: 200
  },
  {
    _id: { customer: { name: 'Thomas', city: 'Lviv' }, daypair: 2 },
    subtotal: 200
  },
  {
    _id: { customer: { name: 'John', city: 'Kyiv' }, daypair: 1 },
    subtotal: 250
  },
  {
    _id: { customer: { name: 'Jane', city: 'Kharkiv' }, daypair: 1 },
    subtotal: 605
  }
]
```

Далі групуємо статистику по користувачах
```javascript
A = db.orders.aggregate([
  { 
    $group: { 
      _id: {
        customer: '$customer', 
        daypair: {$ceil: {$divide: [{$dayOfMonth: '$date'}, 2] }},
      }, 
      subtotal: { $sum: '$subtotal' } 
    }
  },
  {
    $group: {
        _id: '$_id.customer.name',
        subtotals: { $addToSet: { daypair: '$_id.daypair', val: '$subtotal' } }
    }
  }
])

[
  { _id: 'John', subtotals: [ { daypair: 1, val: 250 } ] },
  { _id: 'NotThomas', subtotals: [ { daypair: 2, val: 200 } ] },
  { _id: 'Jane', subtotals: [ { daypair: 1, val: 605 } ] },
  { _id: 'Thomas', subtotals: [ { daypair: 1, val: 512 }, { daypair: 2, val: 200 } ] }
]
```

Далі різницю вже варто обчислювати іншими методами (напр. джаваскріптом), бо в бд це буде невиправдано складно.

Наприклад:
```javascript
A.forEach((rec) => {
    console.log("Customer ", rec._id);
    let stats = Object.fromEntries(rec.subtotals.map((v) => {
        return [v.daypair, v.val]
    }));
    let difs = Object.entries(stats).map((v,i) => {
        let prev = 0;
        if (v[0]-1 in stats) { prev = stats[v[0]-1]; }
        return [v[0], v[1] - prev]
    })
    difs.forEach((v) => {
        console.log("> daypair ", v[0], "- difference is ", v[1])
    })
    console.log("---")
})

Customer  John
> daypair  1 - difference is  250
---
Customer  NotThomas
> daypair  2 - difference is  200
---
Customer  Jane
> daypair  1 - difference is  605
---
Customer  Thomas
> daypair  1 - difference is  512
> daypair  2 - difference is  -312
---
```
