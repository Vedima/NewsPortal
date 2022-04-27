from django import template


register = template.Library()


BanWords = ['также', 'любовь', 'спорта']


@register.filter()
def censor(word):
   if type(word) != str:
      return 'Неправильный тип данных'
   j = ''
   k = ''
   #word_el = word.split(' ')
   for i in word:
      if i.isalpha():
         j+= i
      else:
         if j.lower() in BanWords:
            k+= j[0] + ('*' * (len(j)-1)) + ' '
         else:
            k+= j
         j=''
         k+=i
   if j.lower() in BanWords:
      k += j[0] + ('*' * (len(j) - 1)) + ' '
   else:
      k += j
   return k
