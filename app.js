var express = require("express"),
    http = require("http"),
    path = require("path"),
    bodyParser = require("body-parser"),
    cookieParser = require("cookie-parser"),
    static = require("serve-static"),
    errorHandler = require("errorhandler"),
    expressErrorHandler = require("express-error-handler"),
    expressSession = require("express-session");

var mysql = require("mysql");

var pool = mysql.createPool({
    connectionLimit: 10,
    host: "192.168.0.23",
    user: "user",
    password: "password123",
    database: "stockbot",
    debug: false,
});

var app = express();

app.set("port", process.env.PORT || 3000);
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use("/img", express.static(__dirname + "/img"));
app.use("/public", express.static(__dirname + "/public"));
app.use(cookieParser());
app.use(
    expressSession({
        secret: "my key",
        resave: true,
        saveUninitialized: true,
    })
);

var router = express.Router();

/*
router.route("/process/mypage").get(function (req, res) {
    console.log("route /process/mypage");
    if (req.session.user) {
        res.redirect("/public/mypage.html");
    } else {
        res.redirect("/public/login.html");
    }
});
*/

router.route("/process/signup").post(function (req, res) {
    console.log("route /process/signup");

    var param_id = req.body.id || req.query.id;
    var param_pw = req.body.password || req.query.password;
    var param_name = req.body.name || req.query.name;
    var param_email = req.body.email || req.query.email;

    console.log(
        "req Parameter : " +
            param_id +
            ", " +
            param_pw +
            ", " +
            param_name +
            ", " +
            param_email
    );

    if (pool) {
        addUser(
            param_id,
            param_pw,
            param_name,
            param_email,
            function (err, addedUser) {
                if (err) {
                    console.error("Error - addUser : " + err.stack);
                    res.write(
                        "<script>alert('Error! ID already exists')</script>"
                    );
                    res.write(
                        '<script>window.location="/public/login.html"</script>'
                    );
                    res.end();
                    return;
                }
                if (addedUser) {
                    console.dir(addedUser);
                    console.log("inserted " + addedUser.affectedRows + " rows");

                    var insertId = addedUser.insertId;
                    console.log("insert ID: " + insertId);
                    res.write("<script>alert('Success!')</script>");
                    res.write(
                        '<script>window.location="/public/login.html"</script>'
                    );
                    res.end();
                    return;
                } else {
                    res.write("<script>alert('Fail to add user')</script>");
                    res.write(
                        '<script>window.location="/public/signup.html"</script>'
                    );
                    res.end();
                }
            }
        );
    } else {
        res.write("<script>alert('Fail to connect DB')</script>");
        res.write('<script>window.location="/public/signup.html"</script>');
        res.end();
    }
});

router.route("/process/login").post(function (req, res) {
    console.log("route /process/login");

    var param_id = req.body.id || req.query.id;
    var param_pw = req.body.password || req.query.password;

    console.log("req Parameters : " + param_id + ", " + param_pw);

    if (pool) {
        authUser(param_id, param_pw, function (err, rows) {
            if (err) {
                console.error("Error - login : " + err.stack);
                res.write("<script>alert('Error!')</script>");
                res.write(
                    '<script>window.location="/public/login.html"</script>'
                );
                res.end();
                return;
            }
            if (rows) {
                console.dir(rows);
                console.log(
                    "id : " + rows[0].id + "    name : " + rows[0].name
                );
                req.session.user = {
                    id: rows[0].id,
                    name: rows[0].name,
                    authorized: true,
                };
                /*
                res.writeHead(200, {
                    "Content-Type": "text/html;characterset=utf8",
                });
                res.write("<h1>Login success!</h1>");
                res.write("[ID] : " + rows[0].id + " [name] : " + rows[0].name + " [email] :: " + rows[0].email);
                res.write('<a href="/process/logout">Logout</a>');
                res.end();
*/
                res.redirect("/public/logout.html");
                return;
            } else {
                res.write("<script>alert('Fail to login.')</script>");
                res.write(
                    '<script>window.location="/public/login.html"</script>'
                );
                res.end();
            }
        });
    } else {
        res.json({ result: "pwfalse" });
        res.write("<script>alert('Fail to connect DB')</script>");
        res.write('<script>window.location="/public/signup.html"</script>');
        res.end();
    }
});
router.route("/process/logout").get(function (req, res) {
    if (req.session.user) {
        console.log("logout");
        req.session.destroy(function (err) {
            if (err) throw err;
            console.log("destroy session and logout");
            res.redirect("/public/index.html");
        });
    } else {
        console.log("Not login user");
        res.redirect("/public/index.html");
    }
});
app.use("/", router);

var addUser = function (id, password, name, email, callback) {
    console.log("addUser");

    pool.getConnection(function (err, conn) {
        console.log("getConnection");
        if (err) {
            if (conn) {
                conn.release((error) => (error ? reject(error) : resolve()));
            }
            callback(err, null);
            return;
        }

        console.log("DB connection thread ID : " + conn.threadId);

        var data = { id: id, password: password, name: name, email: email };

        var exec = conn.query(
            "insert into user set ?",
            data,
            function (err, result) {
                conn.release((error) => (error ? reject(error) : resolve()));
                console.log("SQL: " + exec.sql);

                if (err) {
                    console.log("Error - SQL");
                    console.dir(err);
                    callback(err, null);
                    return;
                }
                callback(null, result);
            }
        );
    });
};

var authUser = function (id, password, callback) {
    console.log("authUser");

    pool.getConnection(function (err, conn) {
        if (err) {
            if (conn) {
                conn.release((error) => (error ? reject(error) : resolve()));
            }
            callback(err, null);
            return;
        }

        console.log("DB connection thread ID : " + conn.threadId);

        var col = ["id", "name", "email"];
        var tablename = "user";

        var exec = conn.query(
            "select ?? from ?? where id = ? and password = ?",
            [col, tablename, id, password],
            function (err, rows) {
                conn.release((error) => (error ? reject(error) : resolve()));
                console.log("SQL: " + exec.sql);

                if (err) throw err;

                if (rows.length > 0) {
                    console.log("ID [%s], pw [%s] User find!", id, password);
                    callback(null, rows);
                } else {
                    console.log("No such user.");
                    callback(null, null);
                }
            }
        );
    });
};

/*
// 404 error
var errorHandler = expressErrorHandler({
    static: {
        404: "/public/404.html",
    },
});

app.use(expressErrorHandler.httpError(404));
app.use(errorHandler);
*/

//웹서버 생성
var appServer = http.createServer(app);
appServer.listen(app.get("port"), function () {
    console.log("express server started with port " + app.get("port"));
});
