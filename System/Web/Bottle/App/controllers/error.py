
def custom500(error):
    return 'Nothing here, here the problem:' + error

handler = {
    500: custom500,
}