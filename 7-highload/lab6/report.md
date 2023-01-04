# 7-Highload. Lab6.
Mykhailo Koreshkov, FI-91

## 1. Cluster setup
```
(sci) PS C:\Windows\system32> docker run --name mongo-primary -d --net mongonet mongo --replSet "rs0"
Unable to find image 'mongo:latest' locally
latest: Pulling from library/mongo
ef773e84b43a: Pull complete
2bfad1efb664: Pull complete
84e59a6d63c9: Pull complete
d2f00ac700e0: Pull complete
96d33bf42f45: Pull complete
ebaa69d77b61: Pull complete
aa77b709a7d6: Pull complete
245bd0c9ace2: Pull complete
Digest: sha256:c015870b10451c414911aff5648495bd3fcc9fe0cec340f46bb852706697a72f
Status: Downloaded newer image for mongo:latest
d306ca7a7d51f81cf5e0a072f4e34c1347886c1ee7a8c84cd524c29c34bb9f80
(sci) PS C:\Windows\system32> docker run --name mongo-1 -d --net mongonet mongo --replSet "rs0"
3947a26f3844011962e0b1cc7af5e1c8d1ba13cd737dd3697f247deb85aa0599
(sci) PS C:\Windows\system32> docker run --name mongo-2 -d --net mongonet mongo --replSet "rs0"
a18c5e25713e9d45c5784acda32c9643ae8890fbca854955f2b01377998a48e3
(sci) PS C:\Windows\system32> docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS       NAMES
a18c5e25713e   mongo     "docker-entrypoint.s…"   6 seconds ago    Up 4 seconds    27017/tcp   mongo-2
3947a26f3844   mongo     "docker-entrypoint.s…"   12 seconds ago   Up 10 seconds   27017/tcp   mongo-1
d306ca7a7d51   mongo     "docker-entrypoint.s…"   43 seconds ago   Up 39 seconds   27017/tcp   mongo-primary
(sci) PS C:\Windows\system32> docker run --name mongo-client -d --net mongonet mongoclient/mongoclient
Unable to find image 'mongoclient/mongoclient:latest' locally
latest: Pulling from mongoclient/mongoclient
290431e50016: Pull complete
6d69d403d242: Pull complete
66a5bb5b2377: Pull complete
814c8cc3a6fa: Pull complete
9f2c20557b72: Pull complete
4e4768f54d55: Pull complete
0312d8fbddab: Pull complete
7e87bd0aff9b: Pull complete
Digest: sha256:ca98c95de349493fab630ca3fae6e611e27e392ebc59f14d7dd73580c045927a
Status: Downloaded newer image for mongoclient/mongoclient:latest
6ea68ab3fdcfc1db33be7c889e762dba1070533bfe93fa374b69075a31f070f1
```

Creating an rsconf from existing mongo containers:
```
rsconf = {_id: "rs0", members: [
    {_id: 0, host: "mongo-primary:27017"},
    {_id: 1, host: "mongo-1:27017"},
    {_id: 2, host: "mongo-2:27017"}
]}
```

Execution:
```
test> rs.initiate(rsconf)
{ ok: 1 }

rs0 [direct: other] test> rs.conf()
```
<details>
<summary>rs.conf() output</summary>
<pre>
{
  _id: 'rs0',
  version: 1,
  term: 1,
  members: [
    {
      _id: 0,
      host: 'mongo-primary:27017',
      arbiterOnly: false,
      buildIndexes: true,
      hidden: false,
      priority: 1,
      tags: {},
      secondaryDelaySecs: Long("0"),
      votes: 1
    },
    {
      _id: 1,
      host: 'mongo-1:27017',
      arbiterOnly: false,
      buildIndexes: true,
      hidden: false,
      priority: 1,
      tags: {},
      secondaryDelaySecs: Long("0"),
      votes: 1
    },
    {
      _id: 2,
      host: 'mongo-2:27017',
      arbiterOnly: false,
      buildIndexes: true,
      hidden: false,
      priority: 1,
      tags: {},
      secondaryDelaySecs: Long("0"),
      votes: 1
    }
  ],
  protocolVersion: Long("1"),
  writeConcernMajorityJournalDefault: true,
  settings: {
    chainingAllowed: true,
    heartbeatIntervalMillis: 2000,
    heartbeatTimeoutSecs: 10,
    electionTimeoutMillis: 10000,
    catchUpTimeoutMillis: -1,
    catchUpTakeoverDelayMillis: 30000,
    getLastErrorModes: {},
    getLastErrorDefaults: { w: 1, wtimeout: 0 },
    replicaSetId: ObjectId("63b4a9ca8657c4207c592bb6")
  }
}

</pre>
</details>

<br>

```
rs0 [direct: primary] test> rs.status()
```

<details>
<summary>rs.status() output</summary>
<pre>
{
  set: 'rs0',
  date: ISODate("2023-01-03T22:25:17.622Z"),
  myState: 1,
  term: Long("1"),
  syncSourceHost: '',
  syncSourceId: -1,
  heartbeatIntervalMillis: Long("2000"),
  majorityVoteCount: 2,
  writeMajorityCount: 2,
  votingMembersCount: 3,
  writableVotingMembersCount: 3,
  optimes: {
    lastCommittedOpTime: { ts: Timestamp({ t: 1672784710, i: 1 }), t: Long("1") },
    lastCommittedWallTime: ISODate("2023-01-03T22:25:10.780Z"),
    readConcernMajorityOpTime: { ts: Timestamp({ t: 1672784710, i: 1 }), t: Long("1") },
    appliedOpTime: { ts: Timestamp({ t: 1672784710, i: 1 }), t: Long("1") },
    durableOpTime: { ts: Timestamp({ t: 1672784710, i: 1 }), t: Long("1") },
    lastAppliedWallTime: ISODate("2023-01-03T22:25:10.780Z"),
    lastDurableWallTime: ISODate("2023-01-03T22:25:10.780Z")
  },
  lastStableRecoveryTimestamp: Timestamp({ t: 1672784680, i: 1 }),
  electionCandidateMetrics: {
    lastElectionReason: 'electionTimeout',
    lastElectionDate: ISODate("2023-01-03T22:19:00.691Z"),
    electionTerm: Long("1"),
    lastCommittedOpTimeAtElection: { ts: Timestamp({ t: 1672784330, i: 1 }), t: Long("-1") },
    lastSeenOpTimeAtElection: { ts: Timestamp({ t: 1672784330, i: 1 }), t: Long("-1") },
    numVotesNeeded: 2,
    priorityAtElection: 1,
    electionTimeoutMillis: Long("10000"),
    numCatchUpOps: Long("0"),
    newTermStartDate: ISODate("2023-01-03T22:19:00.745Z"),
    wMajorityWriteAvailabilityDate: ISODate("2023-01-03T22:19:02.062Z")
  },
  members: [
    {
      _id: 0,
      name: 'mongo-primary:27017',
      health: 1,
      state: 1,
      stateStr: 'PRIMARY',
      uptime: 951,
      optime: { ts: Timestamp({ t: 1672784710, i: 1 }), t: Long("1") },
      optimeDate: ISODate("2023-01-03T22:25:10.000Z"),
      lastAppliedWallTime: ISODate("2023-01-03T22:25:10.780Z"),
      lastDurableWallTime: ISODate("2023-01-03T22:25:10.780Z"),
      syncSourceHost: '',
      syncSourceId: -1,
      infoMessage: '',
      electionTime: Timestamp({ t: 1672784340, i: 1 }),
      electionDate: ISODate("2023-01-03T22:19:00.000Z"),
      configVersion: 1,
      configTerm: 1,
      self: true,
      lastHeartbeatMessage: ''
    },
    {
      _id: 1,
      name: 'mongo-1:27017',
      health: 1,
      state: 2,
      stateStr: 'SECONDARY',
      uptime: 387,
      optime: { ts: Timestamp({ t: 1672784710, i: 1 }), t: Long("1") },
      optimeDurable: { ts: Timestamp({ t: 1672784710, i: 1 }), t: Long("1") },
      optimeDate: ISODate("2023-01-03T22:25:10.000Z"),
      optimeDurableDate: ISODate("2023-01-03T22:25:10.000Z"),
      lastAppliedWallTime: ISODate("2023-01-03T22:25:10.780Z"),
      lastDurableWallTime: ISODate("2023-01-03T22:25:10.780Z"),
      lastHeartbeat: ISODate("2023-01-03T22:25:16.812Z"),
      lastHeartbeatRecv: ISODate("2023-01-03T22:25:16.280Z"),
      pingMs: Long("0"),
      lastHeartbeatMessage: '',
      syncSourceHost: 'mongo-primary:27017',
      syncSourceId: 0,
      infoMessage: '',
      configVersion: 1,
      configTerm: 1
    },
    {
      _id: 2,
      name: 'mongo-2:27017',
      health: 1,
      state: 2,
      stateStr: 'SECONDARY',
      uptime: 387,
      optime: { ts: Timestamp({ t: 1672784710, i: 1 }), t: Long("1") },
      optimeDurable: { ts: Timestamp({ t: 1672784710, i: 1 }), t: Long("1") },
      optimeDate: ISODate("2023-01-03T22:25:10.000Z"),
      optimeDurableDate: ISODate("2023-01-03T22:25:10.000Z"),
      lastAppliedWallTime: ISODate("2023-01-03T22:25:10.780Z"),
      lastDurableWallTime: ISODate("2023-01-03T22:25:10.780Z"),
      lastHeartbeat: ISODate("2023-01-03T22:25:16.812Z"),
      lastHeartbeatRecv: ISODate("2023-01-03T22:25:16.280Z"),
      pingMs: Long("0"),
      lastHeartbeatMessage: '',
      syncSourceHost: 'mongo-primary:27017',
      syncSourceId: 0,
      infoMessage: '',
      configVersion: 1,
      configTerm: 1
    }
  ],
  ok: 1,
  '$clusterTime': {
    clusterTime: Timestamp({ t: 1672784710, i: 1 }),
    signature: {
      hash: Binary(Buffer.from("0000000000000000000000000000000000000000", "hex"), 0),
      keyId: Long("0")
    }
  },
  operationTime: Timestamp({ t: 1672784710, i: 1 })
}
</pre>
</details>

<br>

Далі створюємо коллекцію

```
(sci) PS C:\Windows\system32> docker exec -it mongo-client bash
node@6ea68ab3fdcf:/opt/meteor/dist/bundle$ mongo mongo-primary:27017

MongoDB shell version v4.2.10-17-g872b733
connecting to: mongodb://mongo-primary:27017/test?compressors=disabled&gssapiServiceName=mongodb
...
...

rs0:PRIMARY> use lab6
switched to db lab6

rs0:PRIMARY> db.createCollection("A")
{
        "ok" : 1,
        "$clusterTime" : {
                "clusterTime" : Timestamp(1672786250, 1),
                "signature" : {
                        "hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
                        "keyId" : NumberLong(0)
                }
        },
        "operationTime" : Timestamp(1672786250, 1)
}

```

Та заповнюємо її чимось

```
rs0:PRIMARY> db.A.find()
{ "_id" : ObjectId("63b4b2450855638ee47c0fd8"), "text" : "lorem ipsum 1", "num" : 192, "data" : [ "a", "b" ] }
{ "_id" : ObjectId("63b4b2540855638ee47c0fd9"), "text" : "lorem ipsum 2", "num" : 168, "data" : [ "a", "b", "c" ] }
{ "_id" : ObjectId("63b4b2610855638ee47c0fda"), "text" : "lorem ipsum 3", "num" : 0, "data" : [ ] }
{ "_id" : ObjectId("63b4b26d0855638ee47c0fdb"), "text" : "lorem ipsum 4", "num" : -12 }
{ "_id" : ObjectId("63b4b2790855638ee47c0fdc"), "text" : "lorem ipsum 5", "num" : 1, "data" : [ "d" ] }
```

## 2. Продемонструвати Read Preference Modes: primary, secondary

On primary, readPref primary
```
rs0:PRIMARY> db.getMongo().setReadPref('primary')
rs0:PRIMARY> db.A.find()
{ "_id" : ObjectId("63b4b2450855638ee47c0fd8"), "text" : "lorem ipsum 1", "num" : 192, "data" : [ "a", "b" ] }
{ "_id" : ObjectId("63b4b2540855638ee47c0fd9"), "text" : "lorem ipsum 2", "num" : 168, "data" : [ "a", "b", "c" ] }
{ "_id" : ObjectId("63b4b2610855638ee47c0fda"), "text" : "lorem ipsum 3", "num" : 0, "data" : [ ] }
{ "_id" : ObjectId("63b4b26d0855638ee47c0fdb"), "text" : "lorem ipsum 4", "num" : -12 }
{ "_id" : ObjectId("63b4b2790855638ee47c0fdc"), "text" : "lorem ipsum 5", "num" : 1, "data" : [ "d" ] }
{ "_id" : ObjectId("63b4bc220855638ee47c0fdd"), "text" : "lorem ipsum repl1", "num" : 200, "data" : [ "a", "b", "c" ] }
```

On primary, readPref secondary
```
rs0:PRIMARY> db.getMongo().setReadPref('secondary')
rs0:PRIMARY> db.A.find()
{ "_id" : ObjectId("63b4b2450855638ee47c0fd8"), "text" : "lorem ipsum 1", "num" : 192, "data" : [ "a", "b" ] }
{ "_id" : ObjectId("63b4b2540855638ee47c0fd9"), "text" : "lorem ipsum 2", "num" : 168, "data" : [ "a", "b", "c" ] }
{ "_id" : ObjectId("63b4b2610855638ee47c0fda"), "text" : "lorem ipsum 3", "num" : 0, "data" : [ ] }
{ "_id" : ObjectId("63b4b26d0855638ee47c0fdb"), "text" : "lorem ipsum 4", "num" : -12 }
{ "_id" : ObjectId("63b4b2790855638ee47c0fdc"), "text" : "lorem ipsum 5", "num" : 1, "data" : [ "d" ] }
{ "_id" : ObjectId("63b4bc220855638ee47c0fdd"), "text" : "lorem ipsum repl1", "num" : 200, "data" : [ "a", "b", "c" ] }
```

On secondary, readPref primary (via `mongosh` on a secondary node)
```
rs0 [direct: secondary] lab6> db.getMongo().setReadPref('primary')

rs0 [direct: secondary] lab6> db.A.find()
MongoServerError: not primary and secondaryOk=false - consider using db.getMongo().setReadPref() or readPreference in the connection string
```

On secondary, readPref secondary
```
rs0 [direct: secondary] lab6> db.getMongo().setReadPref('secondary')

rs0 [direct: secondary] lab6> db.A.find()
[
  {
    _id: ObjectId("63b4b2450855638ee47c0fd8"),
    text: 'lorem ipsum 1',
    num: 192,
    data: [ 'a', 'b' ]
  },
  ...
  {
    _id: ObjectId("63b4bc220855638ee47c0fdd"),
    text: 'lorem ipsum repl1',
    num: 200,
    data: [ 'a', 'b', 'c' ]
  }
]
```

## 3. 
Спробувати зробити запис з однією відключеною нодою та write concern рівнім 3 та нескінченім таймаутом. Спробувати під час таймаута включити відключену ноду

Нода `mongo-2` вимкнена.

```
rs0:PRIMARY> db.setWriteConcern({"w":3, wtimeout:0})
rs0:PRIMARY> db.A.insert({text: "1nodedown w3 t0"})
<консоль заблокована, бо нод недостатньо, а таймаут нескінченний>
```
Вмикаю ноду `mongo-2`:
```
WriteResult({ "nInserted" : 1 })
```

## 4. 
Аналогічно попередньому пункту, але задати скінченний таймаут та дочекатись його закінчення. Перевірити чи данні записались і чи доступні на читання з рівнем readConcern: “majority”

Вимикаю ноду `mongo-2`

```
rs0:PRIMARY> db.setWriteConcern({"w":3, wtimeout:5000})
rs0:PRIMARY> db.A.insert({text: "1nodedown w3 t5"})
WriteResult({
        "nInserted" : 1,
        "writeConcernError" : {
                "code" : 64,
                "codeName" : "WriteConcernFailed",
                "errmsg" : "waiting for replication timed out",
                "errInfo" : {
                        "wtimeout" : true,
                        "writeConcern" : {
                                "w" : 3,
                                "wtimeout" : 5000,
                                "provenance" : "clientSupplied"
                        }
                }
        }
})
```

```
rs0:PRIMARY> db.getMongo().setReadPref('primary')
rs0:PRIMARY> db.A.find()
{ "_id" : ObjectId("63b4b2450855638ee47c0fd8"), "text" : "lorem ipsum 1", "num" : 192, "data" : [ "a", "b" ] }
{ "_id" : ObjectId("63b4b2540855638ee47c0fd9"), "text" : "lorem ipsum 2", "num" : 168, "data" : [ "a", "b", "c" ] }
{ "_id" : ObjectId("63b4b2610855638ee47c0fda"), "text" : "lorem ipsum 3", "num" : 0, "data" : [ ] }
{ "_id" : ObjectId("63b4b26d0855638ee47c0fdb"), "text" : "lorem ipsum 4", "num" : -12 }
{ "_id" : ObjectId("63b4b2790855638ee47c0fdc"), "text" : "lorem ipsum 5", "num" : 1, "data" : [ "d" ] }
{ "_id" : ObjectId("63b4bc220855638ee47c0fdd"), "text" : "lorem ipsum repl1", "num" : 200, "data" : [ "a", "b", "c" ] }
{ "_id" : ObjectId("63b4c0640855638ee47c0fde"), "text" : "w3 t0" }
{ "_id" : ObjectId("63b4c0c30855638ee47c0fdf"), "text" : "1nodedown w3 t0" }
{ "_id" : ObjectId("63b4c1630855638ee47c0fe0"), "text" : "1nodedown w3 t5" }
rs0:PRIMARY> db.getMongo().setReadConcern('majority')
rs0:PRIMARY> db.A.find()
{ "_id" : ObjectId("63b4b2450855638ee47c0fd8"), "text" : "lorem ipsum 1", "num" : 192, "data" : [ "a", "b" ] }
{ "_id" : ObjectId("63b4b2540855638ee47c0fd9"), "text" : "lorem ipsum 2", "num" : 168, "data" : [ "a", "b", "c" ] }
{ "_id" : ObjectId("63b4b2610855638ee47c0fda"), "text" : "lorem ipsum 3", "num" : 0, "data" : [ ] }
{ "_id" : ObjectId("63b4b26d0855638ee47c0fdb"), "text" : "lorem ipsum 4", "num" : -12 }
{ "_id" : ObjectId("63b4b2790855638ee47c0fdc"), "text" : "lorem ipsum 5", "num" : 1, "data" : [ "d" ] }
{ "_id" : ObjectId("63b4bc220855638ee47c0fdd"), "text" : "lorem ipsum repl1", "num" : 200, "data" : [ "a", "b", "c" ] }
{ "_id" : ObjectId("63b4c0640855638ee47c0fde"), "text" : "w3 t0" }
{ "_id" : ObjectId("63b4c0c30855638ee47c0fdf"), "text" : "1nodedown w3 t0" }
{ "_id" : ObjectId("63b4c1630855638ee47c0fe0"), "text" : "1nodedown w3 t5" }
```

Читання ок, бо majority для 3 нод значить 2 ноди.

## 5.
Продемонстрував перевибори primary node в відключивши поточний primary (Replica Set Elections)  
І що після відновлення роботи старої primary на неї реплікуються нові дані, які з'явилися під час її простою

```
rs0 [direct: secondary] test> rs.status()
{
  set: 'rs0',
  date: ISODate("2023-01-04T00:10:06.249Z"),
  myState: 2,
  term: Long("2"),
  syncSourceHost: 'mongo-primary:27017',
  syncSourceId: 0,
  heartbeatIntervalMillis: Long("2000"),
  majorityVoteCount: 2,
  writeMajorityCount: 2,
  votingMembersCount: 3,
  writableVotingMembersCount: 3,
  optimes: {
    lastCommittedOpTime: { ts: Timestamp({ t: 1672791000, i: 1 }), t: Long("2") },
    lastCommittedWallTime: ISODate("2023-01-04T00:10:00.581Z"),
    readConcernMajorityOpTime: { ts: Timestamp({ t: 1672791000, i: 1 }), t: Long("2") },
    appliedOpTime: { ts: Timestamp({ t: 1672791000, i: 1 }), t: Long("2") },
    durableOpTime: { ts: Timestamp({ t: 1672791000, i: 1 }), t: Long("2") },
    lastAppliedWallTime: ISODate("2023-01-04T00:10:00.581Z"),
    lastDurableWallTime: ISODate("2023-01-04T00:10:00.581Z")
  },
  lastStableRecoveryTimestamp: Timestamp({ t: 1672790950, i: 1 }),
  electionParticipantMetrics: {
    votedForCandidate: true,
    electionTerm: Long("2"),
    lastVoteDate: ISODate("2023-01-04T00:07:20.560Z"),
    electionCandidateMemberId: 0,
    voteReason: '',
    lastAppliedOpTimeAtElection: { ts: Timestamp({ t: 1672790731, i: 1 }), t: Long("1") },
    maxAppliedOpTimeInSet: { ts: Timestamp({ t: 1672790731, i: 1 }), t: Long("1") },
    priorityAtElection: 1,
    newTermStartDate: ISODate("2023-01-04T00:07:20.575Z"),
    newTermAppliedDate: ISODate("2023-01-04T00:07:20.610Z")
  },
  members: [
    {
      _id: 0,
      name: 'mongo-primary:27017',
      health: 1,
      state: 1,
      stateStr: 'PRIMARY',
      uptime: 172,
      optime: { ts: Timestamp({ t: 1672791000, i: 1 }), t: Long("2") },
      optimeDurable: { ts: Timestamp({ t: 1672791000, i: 1 }), t: Long("2") },
      optimeDate: ISODate("2023-01-04T00:10:00.000Z"),
      optimeDurableDate: ISODate("2023-01-04T00:10:00.000Z"),
      lastAppliedWallTime: ISODate("2023-01-04T00:10:00.581Z"),
      lastDurableWallTime: ISODate("2023-01-04T00:10:00.581Z"),
      lastHeartbeat: ISODate("2023-01-04T00:10:05.120Z"),
      lastHeartbeatRecv: ISODate("2023-01-04T00:10:04.599Z"),
      pingMs: Long("0"),
      lastHeartbeatMessage: '',
      syncSourceHost: '',
      syncSourceId: -1,
      infoMessage: '',
      electionTime: Timestamp({ t: 1672790840, i: 1 }),
      electionDate: ISODate("2023-01-04T00:07:20.000Z"),
      configVersion: 1,
      configTerm: 2
    },
    {
      _id: 1,
      name: 'mongo-1:27017',
      health: 1,
      state: 2,
      stateStr: 'SECONDARY',
      uptime: 174,
      optime: { ts: Timestamp({ t: 1672791000, i: 1 }), t: Long("2") },
      optimeDate: ISODate("2023-01-04T00:10:00.000Z"),
      lastAppliedWallTime: ISODate("2023-01-04T00:10:00.581Z"),
      lastDurableWallTime: ISODate("2023-01-04T00:10:00.581Z"),
      syncSourceHost: 'mongo-primary:27017',
      syncSourceId: 0,
      infoMessage: '',
      configVersion: 1,
      configTerm: 2,
      self: true,
      lastHeartbeatMessage: ''
    },
    {
      _id: 2,
      name: 'mongo-2:27017',
      health: 1,
      state: 2,
      stateStr: 'SECONDARY',
      uptime: 76,
      optime: { ts: Timestamp({ t: 1672791000, i: 1 }), t: Long("2") },
      optimeDurable: { ts: Timestamp({ t: 1672791000, i: 1 }), t: Long("2") },
      optimeDate: ISODate("2023-01-04T00:10:00.000Z"),
      optimeDurableDate: ISODate("2023-01-04T00:10:00.000Z"),
      lastAppliedWallTime: ISODate("2023-01-04T00:10:00.581Z"),
      lastDurableWallTime: ISODate("2023-01-04T00:10:00.581Z"),
      lastHeartbeat: ISODate("2023-01-04T00:10:05.629Z"),
      lastHeartbeatRecv: ISODate("2023-01-04T00:10:05.241Z"),
      pingMs: Long("0"),
      lastHeartbeatMessage: '',
      syncSourceHost: 'mongo-1:27017',
      syncSourceId: 1,
      infoMessage: '',
      configVersion: 1,
      configTerm: 2
    }
  ],
  ok: 1,
  '$clusterTime': {
    clusterTime: Timestamp({ t: 1672791000, i: 1 }),
    signature: {
      hash: Binary(Buffer.from("0000000000000000000000000000000000000000", "hex"), 0),
      keyId: Long("0")
    }
  },
  operationTime: Timestamp({ t: 1672791000, i: 1 })
}
```

Зупиняю `mongo-primary`.
Бачу, що консоль змінила prompt: з `direct: secondary` на `direct: primary`. 
Також оновився статус реплікації та додалася інформація про перевибори:

```
rs0 [direct: primary] test> rs.status()
{
  set: 'rs0',
  date: ISODate("2023-01-04T00:12:56.017Z"),
  myState: 1,
  term: Long("3"),
  syncSourceHost: '',
  syncSourceId: -1,
  heartbeatIntervalMillis: Long("2000"),
  majorityVoteCount: 2,
  writeMajorityCount: 2,
  votingMembersCount: 3,
  writableVotingMembersCount: 3,
  optimes: {
    lastCommittedOpTime: { ts: Timestamp({ t: 1672791167, i: 1 }), t: Long("3") },
    lastCommittedWallTime: ISODate("2023-01-04T00:12:47.459Z"),
    readConcernMajorityOpTime: { ts: Timestamp({ t: 1672791167, i: 1 }), t: Long("3") },
    appliedOpTime: { ts: Timestamp({ t: 1672791167, i: 1 }), t: Long("3") },
    durableOpTime: { ts: Timestamp({ t: 1672791167, i: 1 }), t: Long("3") },
    lastAppliedWallTime: ISODate("2023-01-04T00:12:47.459Z"),
    lastDurableWallTime: ISODate("2023-01-04T00:12:47.459Z")
  },
  lastStableRecoveryTimestamp: Timestamp({ t: 1672791133, i: 3 }),
  electionCandidateMetrics: {
    lastElectionReason: 'stepUpRequestSkipDryRun',
    lastElectionDate: ISODate("2023-01-04T00:10:47.443Z"),
    electionTerm: Long("3"),
    lastCommittedOpTimeAtElection: { ts: Timestamp({ t: 1672791040, i: 1 }), t: Long("2") },
    lastSeenOpTimeAtElection: { ts: Timestamp({ t: 1672791040, i: 1 }), t: Long("2") },
    numVotesNeeded: 2,
    priorityAtElection: 1,
    electionTimeoutMillis: Long("10000"),
    priorPrimaryMemberId: 0,
    numCatchUpOps: Long("0"),
    newTermStartDate: ISODate("2023-01-04T00:10:47.454Z"),
    wMajorityWriteAvailabilityDate: ISODate("2023-01-04T00:10:47.457Z")
  },
  electionParticipantMetrics: {
    votedForCandidate: true,
    electionTerm: Long("2"),
    lastVoteDate: ISODate("2023-01-04T00:07:20.560Z"),
    electionCandidateMemberId: 0,
    voteReason: '',
    lastAppliedOpTimeAtElection: { ts: Timestamp({ t: 1672790731, i: 1 }), t: Long("1") },
    maxAppliedOpTimeInSet: { ts: Timestamp({ t: 1672790731, i: 1 }), t: Long("1") },
    priorityAtElection: 1
  },
  members: [
    {
      _id: 0,
      name: 'mongo-primary:27017',
      health: 0,
      state: 8,
      stateStr: '(not reachable/healthy)',
      uptime: 0,
      optime: { ts: Timestamp({ t: 0, i: 0 }), t: Long("-1") },
      optimeDurable: { ts: Timestamp({ t: 0, i: 0 }), t: Long("-1") },
      optimeDate: ISODate("1970-01-01T00:00:00.000Z"),
      optimeDurableDate: ISODate("1970-01-01T00:00:00.000Z"),
      lastAppliedWallTime: ISODate("2023-01-04T00:10:47.454Z"),
      lastDurableWallTime: ISODate("2023-01-04T00:10:47.454Z"),
      lastHeartbeat: ISODate("2023-01-04T00:12:54.248Z"),
      lastHeartbeatRecv: ISODate("2023-01-04T00:10:56.461Z"),
      pingMs: Long("0"),
      lastHeartbeatMessage: 'Error connecting to mongo-primary:27017 :: caused by :: Could not find address for mongo-primary:27017: SocketException: Host not found (authoritative)',
      syncSourceHost: '',
      syncSourceId: -1,
      infoMessage: '',
      configVersion: 1,
      configTerm: 3
    },
    {
      _id: 1,
      name: 'mongo-1:27017',
      health: 1,
      state: 1,
      stateStr: 'PRIMARY',
      uptime: 344,
      optime: { ts: Timestamp({ t: 1672791167, i: 1 }), t: Long("3") },
      optimeDate: ISODate("2023-01-04T00:12:47.000Z"),
      lastAppliedWallTime: ISODate("2023-01-04T00:12:47.459Z"),
      lastDurableWallTime: ISODate("2023-01-04T00:12:47.459Z"),
      syncSourceHost: '',
      syncSourceId: -1,
      infoMessage: '',
      electionTime: Timestamp({ t: 1672791047, i: 1 }),
      electionDate: ISODate("2023-01-04T00:10:47.000Z"),
      configVersion: 1,
      configTerm: 3,
      self: true,
      lastHeartbeatMessage: ''
    },
    {
      _id: 2,
      name: 'mongo-2:27017',
      health: 1,
      state: 2,
      stateStr: 'SECONDARY',
      uptime: 246,
      optime: { ts: Timestamp({ t: 1672791167, i: 1 }), t: Long("3") },
      optimeDurable: { ts: Timestamp({ t: 1672791167, i: 1 }), t: Long("3") },
      optimeDate: ISODate("2023-01-04T00:12:47.000Z"),
      optimeDurableDate: ISODate("2023-01-04T00:12:47.000Z"),
      lastAppliedWallTime: ISODate("2023-01-04T00:12:47.459Z"),
      lastDurableWallTime: ISODate("2023-01-04T00:12:47.459Z"),
      lastHeartbeat: ISODate("2023-01-04T00:12:55.469Z"),
      lastHeartbeatRecv: ISODate("2023-01-04T00:12:55.468Z"),
      pingMs: Long("0"),
      lastHeartbeatMessage: '',
      syncSourceHost: 'mongo-1:27017',
      syncSourceId: 1,
      infoMessage: '',
      configVersion: 1,
      configTerm: 3
    }
  ],
  ok: 1,
  '$clusterTime': {
    clusterTime: Timestamp({ t: 1672791167, i: 1 }),
    signature: {
      hash: Binary(Buffer.from("0000000000000000000000000000000000000000", "hex"), 0),
      keyId: Long("0")
    }
  },
  operationTime: Timestamp({ t: 1672791167, i: 1 })
}
```

Записуємо в бд дані (з консолі `mongo-1`):
```
rs0 [direct: primary] test> db.getMongo().setWriteConcern({w:'majority'})

rs0 [direct: primary] test> db.A.insert({text: "task5 2"})
{
  acknowledged: true,
  insertedIds: { '0': ObjectId("63b4c51cfd61ffd8f2596948") }
}
rs0 [direct: primary] test> db.A.find()
[
  { _id: ObjectId("63b4c4dafd61ffd8f2596947"), text: 'task5 1' },
  { _id: ObjectId("63b4c51cfd61ffd8f2596948"), text: 'task5 2' }
]
```

Тепер вмикаємо `mongo-primary` та читаємо дані на цій ноді:
```
rs0 [direct: secondary] test> db.A.find()
MongoServerError: not primary and secondaryOk=false - consider using db.getMongo().setReadPref() or readPreference in the connection string
rs0 [direct: secondary] test> db.getMongo().setReadPref('secondary')

rs0 [direct: secondary] test> db.A.find()
[
  { _id: ObjectId("63b4c51cfd61ffd8f2596948"), text: 'task5 2' },
  { _id: ObjectId("63b4c4dafd61ffd8f2596947"), text: 'task5 1' }
]
```

Нові дані репліковані

## 6

По-перше, для зручності, поверну статус primary ноді `mongo-primary`.

1. Вимикаю ноди `mongo-1` та `mongo-2`.  
    `mongo-primary` не стає `primary`. Для цього треба увімкнути хоча б одну іншу ноду.  
    Тим не менш, дані все ще читаються.
2. Вмикаю ноду `mongo-1`.  
    Через деякий час відбуваються перевибори. `mongo-primary` стає головною, `mongo-1` стає вторинною.

### 6.1.

Вимкнув ноди `mongo-1`, `mongo-2`. Записав менш ніж за 5 секунд.
```
rs0 [direct: primary] test> db.getMongo().setWriteConcern({w:1})

rs0 [direct: primary] test> db.A.insertOne({text: "task6.1 1"})
{
  acknowledged: true,
  insertedId: ObjectId("63b4c87e423c24192073994a")
}

rs0 [direct: secondary] test> db.getMongo().setReadPref('nearest'); db.A.find()
[
  { _id: ObjectId("63b4c51cfd61ffd8f2596948"), text: 'task5 2' },
  { _id: ObjectId("63b4c4dafd61ffd8f2596947"), text: 'task5 1' },
  { _id: ObjectId("63b4c87e423c24192073994a"), text: 'task6.1 1' }
]
```

### 6.2. Читання із різними read concern

- Majority
    ```
    rs0 [direct: secondary] test> db.getMongo().setReadConcern('majority'); db.A.find()
    [
      { _id: ObjectId("63b4c51cfd61ffd8f2596948"), text: 'task5 2' },
      { _id: ObjectId("63b4c4dafd61ffd8f2596947"), text: 'task5 1' }
    ]
    ```
    Бачимо, що "спірний" документ не потрапив у результат запиту.

- Local
    ```
    rs0 [direct: secondary] test> db.getMongo().setReadConcern('local'); db.A.find()
    [
      { _id: ObjectId("63b4c51cfd61ffd8f2596948"), text: 'task5 2' },
      { _id: ObjectId("63b4c4dafd61ffd8f2596947"), text: 'task5 1' },
      { _id: ObjectId("63b4c87e423c24192073994a"), text: 'task6.1 1' }
    ]
    ```
    Все потрапило в результат.

- Linearizable
    ```
    rs0 [direct: secondary] test> db.getMongo().setReadConcern('linearizable'); db.A.find()
    MongoServerError: afterClusterTime field can be set only if level is equal to majority, local, or snapshot
    ```

### 6.3. 

`mongo-primary`:
```
rs0 [direct: secondary] test> db.getMongo().setReadConcern('local'); db.getMongo().setReadPref('nearest'); db.A.find()
[
  { _id: ObjectId("63b4c51cfd61ffd8f2596948"), text: 'task5 2' },
  { _id: ObjectId("63b4c4dafd61ffd8f2596947"), text: 'task5 1' },
  { _id: ObjectId("63b4c87e423c24192073994a"), text: 'task6.1 1' },
  {
    _id: ObjectId("63b4caf4423c24192073994c"),
    text: 'task6. This will be removed'
  }
]
```

Вимикаємо `mongo-primary`, вмикаємо дві інші.

`mongo-1`:
```
rs0 [direct: secondary] test> rs.status()
{
  set: 'rs0',
  date: ISODate("2023-01-04T00:42:41.281Z"),
  myState: 2,
  term: Long("9"),
  syncSourceHost: 'mongo-2:27017',
  syncSourceId: 2,
  heartbeatIntervalMillis: Long("2000"),
  majorityVoteCount: 2,
  writeMajorityCount: 2,
  votingMembersCount: 3,
  writableVotingMembersCount: 3,
  optimes: {
    lastCommittedOpTime: { ts: Timestamp({ t: 1672792956, i: 2 }), t: Long("9") },
    lastCommittedWallTime: ISODate("2023-01-04T00:42:36.369Z"),
    readConcernMajorityOpTime: { ts: Timestamp({ t: 1672792956, i: 2 }), t: Long("9") },
    appliedOpTime: { ts: Timestamp({ t: 1672792956, i: 2 }), t: Long("9") },
    durableOpTime: { ts: Timestamp({ t: 1672792956, i: 2 }), t: Long("9") },
    lastAppliedWallTime: ISODate("2023-01-04T00:42:36.369Z"),
    lastDurableWallTime: ISODate("2023-01-04T00:42:36.369Z")
  },
  lastStableRecoveryTimestamp: Timestamp({ t: 1672792700, i: 1 }),
  electionParticipantMetrics: {
    votedForCandidate: true,
    electionTerm: Long("9"),
    lastVoteDate: ISODate("2023-01-04T00:42:36.356Z"),
    electionCandidateMemberId: 2,
    voteReason: '',
    lastAppliedOpTimeAtElection: { ts: Timestamp({ t: 1672792815, i: 1 }), t: Long("8") },
    maxAppliedOpTimeInSet: { ts: Timestamp({ t: 1672792815, i: 1 }), t: Long("8") },
    priorityAtElection: 1,
    newTermStartDate: ISODate("2023-01-04T00:42:36.369Z"),
    newTermAppliedDate: ISODate("2023-01-04T00:42:37.055Z")
  },
  members: [
    {
      _id: 0,
      name: 'mongo-primary:27017',
      health: 0,
      state: 8,
      stateStr: '(not reachable/healthy)',
      uptime: 0,
      optime: { ts: Timestamp({ t: 0, i: 0 }), t: Long("-1") },
      optimeDurable: { ts: Timestamp({ t: 0, i: 0 }), t: Long("-1") },
      optimeDate: ISODate("1970-01-01T00:00:00.000Z"),
      optimeDurableDate: ISODate("1970-01-01T00:00:00.000Z"),
      lastAppliedWallTime: ISODate("1970-01-01T00:00:00.000Z"),
      lastDurableWallTime: ISODate("1970-01-01T00:00:00.000Z"),
      lastHeartbeat: ISODate("2023-01-04T00:42:39.411Z"),
      lastHeartbeatRecv: ISODate("1970-01-01T00:00:00.000Z"),
      pingMs: Long("0"),
      lastHeartbeatMessage: 'Error connecting to mongo-primary:27017 :: caused by :: Could not find address for mongo-primary:27017: SocketException: Host not found (authoritative)',
      syncSourceHost: '',
      syncSourceId: -1,
      infoMessage: '',
      configVersion: -1,
      configTerm: -1
    },
    {
      _id: 1,
      name: 'mongo-1:27017',
      health: 1,
      state: 2,
      stateStr: 'SECONDARY',
      uptime: 16,
      optime: { ts: Timestamp({ t: 1672792956, i: 2 }), t: Long("9") },
      optimeDate: ISODate("2023-01-04T00:42:36.000Z"),
      lastAppliedWallTime: ISODate("2023-01-04T00:42:36.369Z"),
      lastDurableWallTime: ISODate("2023-01-04T00:42:36.369Z"),
      syncSourceHost: 'mongo-2:27017',
      syncSourceId: 2,
      infoMessage: '',
      configVersion: 1,
      configTerm: 9,
      self: true,
      lastHeartbeatMessage: ''
    },
    {
      _id: 2,
      name: 'mongo-2:27017',
      health: 1,
      state: 1,
      stateStr: 'PRIMARY',
      uptime: 15,
      optime: { ts: Timestamp({ t: 1672792956, i: 2 }), t: Long("9") },
      optimeDurable: { ts: Timestamp({ t: 1672792956, i: 2 }), t: Long("9") },
      optimeDate: ISODate("2023-01-04T00:42:36.000Z"),
      optimeDurableDate: ISODate("2023-01-04T00:42:36.000Z"),
      lastAppliedWallTime: ISODate("2023-01-04T00:42:36.369Z"),
      lastDurableWallTime: ISODate("2023-01-04T00:42:36.369Z"),
      lastHeartbeat: ISODate("2023-01-04T00:42:39.374Z"),
      lastHeartbeatRecv: ISODate("2023-01-04T00:42:40.369Z"),
      pingMs: Long("0"),
      lastHeartbeatMessage: '',
      syncSourceHost: '',
      syncSourceId: -1,
      infoMessage: '',
      electionTime: Timestamp({ t: 1672792956, i: 1 }),
      electionDate: ISODate("2023-01-04T00:42:36.000Z"),
      configVersion: 1,
      configTerm: 9
    }
  ],
  ok: 1,
  '$clusterTime': {
    clusterTime: Timestamp({ t: 1672792956, i: 2 }),
    signature: {
      hash: Binary(Buffer.from("0000000000000000000000000000000000000000", "hex"), 0),
      keyId: Long("0")
    }
  },
  operationTime: Timestamp({ t: 1672792956, i: 2 })
}

rs0 [direct: secondary] test> db.getMongo().setReadConcern('local'); db.getMongo().setReadPref('nearest'); db.A.find()
[
  { _id: ObjectId("63b4c4dafd61ffd8f2596947"), text: 'task5 1' },
  { _id: ObjectId("63b4c51cfd61ffd8f2596948"), text: 'task5 2' },
  { _id: ObjectId("63b4c87e423c24192073994a"), text: 'task6.1 1' }
]
```

Вмикаємо назад `mongo-primary` та читаємо дані:
```
rs0 [direct: secondary] test> db.getMongo().setReadPref('nearest'); db.A.find()
[
  { _id: ObjectId("63b4c51cfd61ffd8f2596948"), text: 'task5 2' },
  { _id: ObjectId("63b4c4dafd61ffd8f2596947"), text: 'task5 1' },
  { _id: ObjectId("63b4c87e423c24192073994a"), text: 'task6.1 1' }
]
```

Запис видалився, бо більшість не змогла його підтвердити.

## 7. Земулювати eventual consistency за допомогою установки затримки реплікації для репліки

Робимо `mongo-2` Delayed Replica Set Member з затримкою 30 секунд.
```
rs0 [direct: primary] test> conf.members[2].hidden = true;
true
rs0 [direct: primary] test> conf.members[2].priority = 0;
0
rs0 [direct: primary] test> conf.members[2].votes = 1;
1
rs0 [direct: primary] test> conf.members[2].secondaryDelaySecs = 30;
60
rs0 [direct: primary] test> rs.reconfig(conf)
{
  ok: 1,
  '$clusterTime': {
    clusterTime: Timestamp({ t: 1672793560, i: 1 }),
    signature: {
      hash: Binary(Buffer.from("0000000000000000000000000000000000000000", "hex"), 0),
      keyId: Long("0")
    }
  },
  operationTime: Timestamp({ t: 1672793560, i: 1 })
}
```

## 8. Лишити primary та secondary  для якої налаштована затримка реплікації. Записати декілька значень.
Спробувати прочитати значення з readConcern: {level: "linearizable"}.  
Має бути затримка поки значення не реплікуються на більшість нод.

Зупиняю `mongo-1`.

Записую нові дані:
```
rs0 [direct: primary] test> db.A.insertOne({text: "task8 1", number: 1})
<ЗАТРИМКА В 30 СЕКУНД>
{
  acknowledged: true,
  insertedId: ObjectId("63b4ced0efd8834684c84562")
}
```

Читаю дані:
```
rs0 [direct: primary] test> db.getMongo().setReadConcern('linearizable')

rs0 [direct: primary] test> db.A.find()
<ЗАТРИМКА В 30 СЕКУНД>
[
  { _id: ObjectId("63b4c51cfd61ffd8f2596948"), text: 'task5 2' },
  { _id: ObjectId("63b4c4dafd61ffd8f2596947"), text: 'task5 1' },
  { _id: ObjectId("63b4c87e423c24192073994a"), text: 'task6.1 1' },
  {
    _id: ObjectId("63b4ceacefd8834684c84561"),
    text: 'task8 1',
    number: 1
  },
  {
    _id: ObjectId("63b4ced0efd8834684c84562"),
    text: 'task8 1',
    number: 1
  }
]
```

Додатковий тест:

```
rs0 [direct: primary] test> db.getMongo().setWriteConcern({w:1}); db.A.insertOne({text: "task8 2", number: 1})
{
  acknowledged: true,
  insertedId: ObjectId("63b4d210efd8834684c84563")
}
rs0 [direct: primary] test> db.getMongo().setReadConcern('majority'); db.A.find()
[
  {
    _id: ObjectId("63b4ced0efd8834684c84562"),
    text: 'task8 1',
    number: 1
  }
]
rs0 [direct: primary] test> db.getMongo().setReadConcern('local'); db.A.find()
[
  {
    _id: ObjectId("63b4ced0efd8834684c84562"),
    text: 'task8 1',
    number: 1
  },
  {
    _id: ObjectId("63b4d210efd8834684c84563"),
    text: 'task8 2',
    number: 1
  }
]

<ЧЕКАЮ 30 СЕКУНД>

rs0 [direct: primary] test> db.getMongo().setReadConcern('majority'); db.A.find()
[
  {
    _id: ObjectId("63b4ced0efd8834684c84562"),
    text: 'task8 1',
    number: 1
  },
  {
    _id: ObjectId("63b4d210efd8834684c84563"),
    text: 'task8 2',
    number: 1
  }
]

```

