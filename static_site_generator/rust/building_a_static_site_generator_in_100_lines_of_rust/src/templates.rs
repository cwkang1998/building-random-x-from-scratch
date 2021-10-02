pub const HEADER: &str = r#"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta chartset="utf-8">
    <meta>
</head>
"#;

pub fn render_body(body: &str) -> String {
    format!(
        r#"
        <body>
        <nav>
            <a href='/'>Home</a>
        </nav>
        <br/>
        {}
        </body>"#,
        body
    )
}

pub const FOOTER: &str = r#"
</html>
"#;
