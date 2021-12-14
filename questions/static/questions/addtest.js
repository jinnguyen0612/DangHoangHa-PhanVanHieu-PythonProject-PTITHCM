//var count =0;
//var faqs_row = 0;
var a = ['1','2','3','4'];
function addfaqs() {
    html = '<tr id="faqs-row' + faqs_row + '">';
    html += '<td><input type="text" class="form-control" placeholder="Chosen" name="chosen" id="chosen" required minlength="1" ></td>';
    html += `<td><input required minlength="1" class="radio_animated" id="edo-ani answer" type="radio" name="is_Answer" value=${count}></td>`;
    html += '<td class="mt-10"><button class="badge badge-danger" onclick="$(\'#faqs-row' + faqs_row + '\').remove(); count--; faqs_row++;"><i class="fa fa-trash"></i> Delete</button></td>';
    html += '</tr>';

$('#faqs tbody').append(html);
count++;
faqs_row++;
}

function addfaqs2() {
    html = '<tr id="faqs-row' + faqs_row + '">';
    html += `<td><input  value=${a} type="text" class="form-control" placeholder="Chosen" name="chosen" id="chosen" ></td>`;
    html += `<td><input class="radio_animated" id="edo-ani answer" type="radio" name="is_Answer" value=${count}></td>`;
    html += '<td class="mt-10"><button class="badge badge-danger" onclick="$(\'#faqs-row' + faqs_row + '\').remove(); count--; faqs_row++;"><i class="fa fa-trash"></i> Delete</button></td>';
    html += '</tr>';

$('#faqs tbody').append(html);
count++;
faqs_row++;
}


function getValue(){
    var arr = $('input[name=chosen').map(function(){
        return this.value;
    }).get();
    document.getElementById('answer_list').value=arr;
    document.getElementById('correct_answer').value=$(":radio:checked").val();
    var tam = document.getElementById('input-Question').value;
    document.getElementById('question').value = tam;
    console.log(tam);
    console.log(arr);
    console.log($(":radio:checked").val());
}