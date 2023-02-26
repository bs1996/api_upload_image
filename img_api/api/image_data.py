from .models import Images, Customer, Tiers
import cv2
import os


def convert_to_binary(imglink, number):
    p = os.path.abspath('..')
    imglink2 = imglink[1:]
    link = os.path.join(p, 'img_api', 'api', imglink2)
    directory = os.path.join(p, 'img_api', 'api', 'media', 'images')
    img = cv2.imread(link)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, bin_image = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
    bin_number = str(number) + 'bin.png'
    os.chdir(directory)
    cv2.imwrite(bin_number, bin_image)
    img_directory = os.path.join(p, 'img_api', 'api', 'media', 'images', bin_number)
    return img_directory


def basic(current_user, image):
    add_image = Images(User_id=current_user.id)
    add_image.save()
    add_image = Images.objects.latest('id')
    add_image.number = add_image.id
    add_image.link2 = 'http://127.0.0.1:8000/images/image/' + str(current_user.id) + '/'\
                      + str(add_image.number) + '/200/'
    add_image.image = image
    add_image.save()
    links = [add_image.link2]
    return links


def premium(current_user, image):
    add_image = Images(User_id=current_user.id)
    add_image.save()
    add_image = Images.objects.latest('id')
    add_image.number = add_image.id
    add_image.link1 = 'http://127.0.0.1:8000/images/image/' + str(current_user.id) + '/'\
                      + str(add_image.number) + '/org/'
    add_image.link2 = 'http://127.0.0.1:8000/images/image/' + str(current_user.id) + '/'\
                      + str(add_image.number) + '/200/'
    add_image.link3 = 'http://127.0.0.1:8000/images/image/' + str(current_user.id) + '/'\
                      + str(add_image.number) + '/400/'

    add_image.image = image
    add_image.save()
    links = [add_image.link1, add_image.link2, add_image.link3]
    return links


def enterprise(current_user, image):
    add_image = Images(User_id=current_user.id)
    add_image.save()
    add_image = Images.objects.latest('id')
    add_image.number = add_image.id
    add_image.link1 = 'http://127.0.0.1:8000/images/image/' + str(current_user.id) + '/'\
                      + str(add_image.number) + '/org/'
    add_image.link2 = 'http://127.0.0.1:8000/images/image/' + str(current_user.id) + '/'\
                      + str(add_image.number) + '/200/'
    add_image.link3 = 'http://127.0.0.1:8000/images/image/' + str(current_user.id) + '/'\
                      + str(add_image.number) + '/400/'

    add_image.image = image
    add_image.save()

    links = [add_image.link1, add_image.link2, add_image.link3, add_image.link4]
    return links


def non_standard(current_user, image):
    customer = Customer.objects.filter(user_id=current_user.id)
    account_id = customer[0].account_type_id
    account = Tiers.objects.filter(id=account_id)
    original_file = account[0].original_file
    thumbnail_size = account[0].thumbnail_size

    add_image = Images(User_id=current_user.id)
    add_image.save()
    add_image = Images.objects.latest('id')
    add_image.number = add_image.id
    if original_file:
        add_image.link1 = 'http://127.0.0.1:8000/images/image/' + str(current_user.id) + '/' \
                        + str(add_image.number) + '/org/'
    else:
        add_image.link1 = ''
    add_image.link4 = 'http://127.0.0.1:8000/images/image/' + str(current_user.id) + '/' \
                      + str(add_image.number) + '/' + str(thumbnail_size) + '/'


    add_image.image = image
    add_image.save()

    links = [add_image.link1, add_image.link4]
    return links


def image_data(current_user, image):
    customer = Customer.objects.filter(user_id=current_user.id)
    account_type = customer[0].account_type_id
    if account_type == 1:
        links = basic(current_user, image)
        return links
    if account_type == 2:
        links = premium(current_user, image)
        return links
    if account_type == 3:
        links = enterprise(current_user, image)
        return links
    if account_type > 3:
        links = non_standard(current_user, image)
        return links


def image_link(current_user, number, type):

    images = Images.objects.filter(number=number)
    image = images[0].image

    if type == 'org':
        height = '100%'
        return image, height

    if type == '200':
        height = '200px'
        return image, height

    if type == '400':
        height = '400px'
        return image, height

    else:
        height = str(type) + 'px'
        return image, height



