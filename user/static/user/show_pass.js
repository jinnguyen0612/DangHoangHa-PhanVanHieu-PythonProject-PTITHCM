const ipnElement = document.querySelector('#password')
const ipnElement2 = document.querySelector('#password2')
const btnElement = document.querySelector('#btnPassword')
const btnElement1 = document.querySelector('#btnPassword1')

btnElement.addEventListener('click', function() {

  const currentType = ipnElement.getAttribute('type')

  ipnElement.setAttribute(
    'type',
    currentType === 'password' ? 'text' : 'password'
  )
})

btnElement1.addEventListener('click', function() {

  const currentType = ipnElement2.getAttribute('type')

  ipnElement2.setAttribute(
    'type',
    currentType === 'password' ? 'text' : 'password'
  )
})
