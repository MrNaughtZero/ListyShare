function editListName(){
    document.getElementsByClassName('view-list-top-left')[0].style.display = 'none';
    document.getElementsByClassName('view-list-top-right')[0].style.display = 'none';
    document.getElementsByClassName('view-list-edit-title')[0].style.display = 'flex';
}

function cancelNameChange(){
    document.getElementsByClassName('view-list-top-left')[0].style.display = 'block';
    document.getElementsByClassName('view-list-top-right')[0].style.display = 'block';
    document.getElementsByClassName('view-list-edit-title')[0].style.display = 'none';
}

function addListItem(){
    document.getElementsByClassName('add-items-btns')[0].style.display = 'none';
    document.getElementsByClassName('add-item-form')[0].style.display = 'flex';
}

function addManyItems(){
    document.getElementsByClassName('add-items-btns')[0].style.display = 'none';
    document.getElementsByClassName('add-multiple-items-form')[0].style.display = 'flex';
}

function cancelMultipleListItems(){
    document.getElementsByClassName('add-items-btns')[0].style.display = 'block';
    document.getElementsByClassName('add-multiple-items-form')[0].style.display = 'none';
}

function cancelListItem(){
    document.getElementsByClassName('add-items-btns')[0].style.display = 'block';
    document.getElementsByClassName('add-item-form')[0].style.display = 'none';
}

function deleteListItem(code, link_id, id){
    fetch(`/edit/list/delete/item/${code}/${link_id}/${id}`)
    document.getElementById(`list-item-block-${id}`).style.display = 'none';
}