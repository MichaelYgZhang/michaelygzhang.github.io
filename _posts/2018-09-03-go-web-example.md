---
layout: post
title: Example-Golang-CRUD-Gin
excerpt:  Example-Golang-CRUD-Gin
category: Go
---

####  Example-Golang-CRUD-Gin
- 涉及内容,Golang, http/template, database/sql, go-sql-driver/mysql, net/http, gin;
- 目标: step1完成CRUD，step2结合Gin完成权限管理,文本上传等
##### step 1 完成基本的CRUD

> go get -u github.com/go-sql-driver/mysql //安装依赖

- 创建表

```sql
CREATE TABLE `employee` (
  `id` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
```

- 创建main.go，写CRUD逻辑

```golang
package main

import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	"html/template"
	"net/http"
	"log"
	"strconv"
)

var templ = template.Must(template.ParseGlob("page/*"))

type Employee struct {
	Id int
	Name string
	City string
}

func dbConn() (db *sql.DB)  {
	dbDriver := "mysql"
	dbUser	 := "root"
	dbPasswd := "root123456"
	dbIP	 := "127.0.0.1"
	dbPort   := "3306"
	dbName   := "db_home"
	db, err := sql.Open(dbDriver, dbUser+":"+dbPasswd+"@tcp("+dbIP+":"+dbPort+")/"+dbName)
	if err != nil {
		panic(err.Error())
	}
	return db
}


func Index(w http.ResponseWriter, r *http.Request)  {
	db := dbConn()
	rowsData, err := db.Query("SELECT * FROM EMPLOYEE ORDER BY ID DESC ")
	if err != nil {
		panic(err.Error())
	}
	emp := Employee{}
	res := []Employee{}
	for rowsData.Next() {
		var id int
		var name, city string
		err = rowsData.Scan(&id, &name, &city)
		if err != nil {
			panic(err.Error())
		}
		emp.Id = id
		emp.Name = name
		emp.City = city
		res = append(res, emp)
	}
	templ.ExecuteTemplate(w, "Index", res)
	defer db.Close()
}

func Show(w http.ResponseWriter, r *http.Request)  {
	db := dbConn()
	keyId := r.URL.Query().Get("id")
	rowsData, err := db.Query("SELECT * FROM EMPLOYEE WHERE id=?", keyId)
	if err != nil {
		panic(err.Error())
	}
	emp := Employee{}
	for rowsData.Next() {
		var id int
		var name, city string
		err := rowsData.Scan(&id, &name, &city)
		if err != nil {
			panic(err.Error())
		}
		emp.Id = id
		emp.Name = name
		emp.City = city
	}
	templ.ExecuteTemplate(w, "Show", emp)
	defer db.Close()
}

func New(w http.ResponseWriter, r *http.Request)  {
	templ.ExecuteTemplate(w, "New", nil)
}

func Edit(w http.ResponseWriter, r *http.Request)  {
	db := dbConn()
	keyId := r.URL.Query().Get("id")
	rowsData, err :=db.Query("select * from employee where id=?", keyId)
	if err != nil {
		panic(err.Error())
	}
	emp := Employee{}
	for rowsData.Next() {
		var id int
		var name, city string
		err := rowsData.Scan(&id, &name, &city)
		if err != nil {
			panic(err.Error())
		}
		emp.Id = id
		emp.Name = name
		emp.City = city
	}
	templ.ExecuteTemplate(w, "Edit", emp)
	defer db.Close()
}

func Insert(w http.ResponseWriter, r *http.Request)  {
	db := dbConn()
	if r.Method == "POST" {
		name := r.FormValue("name")
		city := r.FormValue("city")
		stmt, err:= db.Prepare("insert into employee(name,city) values (?,?)")
		if err != nil {
			panic(err.Error())
		}
		result, err := stmt.Exec(name, city)
		if err != nil {
			panic(err.Error())
		}
		LastInsertId, err := result.LastInsertId()
		log.Println("INSERT: Name: " + name +",City: " + city +",LastInsertId:" + strconv.FormatInt(LastInsertId, 10))
	}
	defer db.Close()
	http.Redirect(w, r, "/", 301)
}

func Update(w http.ResponseWriter, r *http.Request) {
	db := dbConn()
	if r.Method == "POST" {
		name := r.FormValue("name")
		city := r.FormValue("city")
		id := r.FormValue("uid")
		insForm, err := db.Prepare("UPDATE Employee SET name=?, city=? WHERE id=?")
		if err != nil {
			panic(err.Error())
		}
		result, e := insForm.Exec(name, city, id)
		if e != nil {
			panic(e.Error())
		}
		RowsAffected, e := result.RowsAffected()
		log.Println("UPDATE: Name: " + name + " | City: " + city +",RowsAffected:"+strconv.FormatInt(RowsAffected, 10))
	}
	defer db.Close()
	http.Redirect(w, r, "/", 301)
}

func Delete(w http.ResponseWriter, r *http.Request) {
	db := dbConn()
	empId := r.URL.Query().Get("id")
	delForm, err := db.Prepare("DELETE FROM Employee WHERE id=?")
	if err != nil {
		panic(err.Error())
	}
	result, e := delForm.Exec(empId)
	if e != nil {
		panic(e.Error())
	}
	RowsAffected, e := result.RowsAffected()
	log.Println("DELETE, id:", empId , ", RowsAffected:"+strconv.FormatInt(RowsAffected, 10))
	defer db.Close()
	http.Redirect(w, r, "/", 301)
}

func main()  {
	log.Println("Server started on: http://localhost:8080")
	http.HandleFunc("/", Index)
	http.HandleFunc("/show", Show)
	http.HandleFunc("/new", New)
	http.HandleFunc("/edit", Edit)
	http.HandleFunc("/insert", Insert)
	http.HandleFunc("/update", Update)
	http.HandleFunc("/delete", Delete)
	http.ListenAndServe(":8080", nil)
}

```

- 创建`page`目录与main.go同级目录,并写好模版


- `Index`

```
{{  define "Index"  }}
    {{  template "Header"    }}
        {{  template "Menu" }}
        <h2> Registered </h2>
        <table border="1">
            <thead>
            <tr>
                <td>ID</td>
                <td>Name</td>
                <td>City</td>
                <td>View</td>
                <td>Edit</td>
                <td>Delete</td>
            </tr>
            </thead>
            <tbody>
            {{  range . }}
            <tr>
                <td>{{  .Id }}</td>
                <td>{{  .Name }}</td>
                <td>{{  .City }}</td>
                <td><a href="/show?id={{    .Id }}">View</a></td>
                <td><a href="/edit?id={{    .Id }}">Edit</a></td>
                <td><a href="/delete?id={{    .Id }}">Del</a></td>
            </tr>
            {{  end }}
        {{ template "Footer" }}
{{  end }}
```

- `Header`

```
{{ define "Header" }}
<!DOCTYPE html>
<html lang="en-US">
    <head>
        <title>Golang Gin Mysql Curd Example</title>
        <meta charset="UTF-8" />
    </head>
    <body>
      <h1>Golang Mysql Curd Example</h1>
{{ end }}
```

- `Menu`

```
{{ define "Menu" }}
    <a href="/">HOME</a> |
    <a href="/new">NEW</a>
{{ end }}
```

- `Footer`

```
{{ define "Footer" }}
    </body>
</html>
{{ end }}
```

- `Show`

```
{{ define "Show" }}
  {{ template "Header" }}
    {{ template "Menu"  }}
    <h2> Register {{ .Id }} </h2>
      <p>Name: {{ .Name }}</p>
      <p>City:  {{ .City }}</p><br /> <a href="/edit?id={{ .Id }}">Edit</a></p>
  {{ template "Footer" }}
{{ end }}
```

- `New`

```
{{ define "New" }}
  {{ template "Header" }}
    {{ template "Menu" }}
   <h2>New Name and City</h2>
    <form method="POST" action="insert">
      <label> Name </label><input type="text" name="name" /><br />
      <label> City </label><input type="text" name="city" /><br />
      <input type="submit" value="Save user" />
    </form>
  {{ template "Footer" }}
{{ end }}
```

- `Edit`

```
{{ define "Edit" }}
  {{ template "Header" }}
    {{ template "Menu" }}
   <h2>Edit Name and City</h2>
    <form method="POST" action="update">
      <input type="hidden" name="uid" value="{{ .Id }}" />
      <label> Name </label><input type="text" name="name" value="{{ .Name }}"  /><br />
      <label> City </label><input type="text" name="city" value="{{ .City }}"  /><br />
      <input type="submit" value="Save user" />
    </form><br />
  {{ template "Footer" }}
{{ end }}
```

##### step2 结合Gin完成权限管理,文本上传等

###### TODO
