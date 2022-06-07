const TemplateEngine = function (tpl: string, data: Record<string, unknown>) {
  const re = /<%([^%>]+)?%>/g; // Regex for variables
  const reExp = /(^( )?(if|for|else|switch|case|break|{|}))(.*)?/g; // Regex for expressions
  let code = 'let r=[];\n';
  let cursor = 0;

  const add = function(line: string, js = false) {
    if(js) {
      if(line.match(reExp)) {
        code += line + '\n';
      } else {
        code += 'r.push(' + line + ');\n';
      }
    } else {
      if(line != '') {
        code += 'r.push("' + line.replace(/"/g, '"') + '");\n';
      } else {
        code += '';
      }
    }
  };

  let match = re.exec(tpl);
  while(match) {
    add(tpl.slice(cursor, match.index));
    add(match[1], true);
    cursor = match.index + match[0].length;
    match = re.exec(tpl);
  }
  // Add remaining string
  add(tpl.substring(cursor, tpl.length));
  code += 'return r.join("");\n'; //return result

  return new Function(code.replace(/[\r\t\n]/g, '')).apply(data);
};

const template = 'Hello my name is <%this.name%>. I\'m <%this.profile.age%> years old.';

console.log(
  TemplateEngine(template, {
    name: 'Krasimir',
    profile: { age: 29 }
  })
);


const template2 = 
  'My skills:' + 
  '<%for(var index in this.skills) {%>' + 
  '<%this.skills[index]%>' +
  '<%}%>';

console.log(TemplateEngine(template2, {
    skills: ['js', 'html', 'css']
}));
